"""
Bots Shiny Application

Test harness for configuring and testing various bot and tool combinations.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import chatlas
from shiny import App, Inputs, Outputs, Session, reactive, req, ui

from tjbots.app.components.sidebar import sidebar_server, sidebar_ui
from tjbots.app.modules.pwa import pwa_ui
from tjbots.app.modules.reconnect import reconnect_ui
from tjbots.config import PackageConfig

config = PackageConfig()

app_dir = Path(__file__).parent
www_tempdir = TemporaryDirectory("tjbots_app_www")
www_dir = Path(www_tempdir.name)
assets_dir = app_dir.parent.parent.parent / "assets"


app_ui = ui.page_sidebar(
    sidebar_ui("sidebar"),
    pwa_ui(
        "pwa",
        png_logo=assets_dir / "logo" / "tjbots.png",
        svg_logo=assets_dir / "logo" / "tjbots.svg",
        www_dir=www_dir,
        app_name="TJBots",
        start_url="https://bots.tjpalanca.com",
        background_color="#000000",
        theme_color="#008080",
        description="TJ's adventures with LLMs",
    ),
    reconnect_ui("reconnect"),
    ui.chat_ui(id="chat"),
    window_title="TJBots",
    fillable=True,
    fillable_mobile=True,
)


def app_server(input: Inputs, output: Outputs, session: Session):
    PackageConfig()
    selected_provider, selected_model = sidebar_server("sidebar")

    # Store chat history to preserve across model changes
    chat_history = reactive.value([])

    @reactive.calc
    def system_prompt():
        return """
            You are TJBot, a helpful AI assistant created by TJ.
            You are knowledgeable, friendly, and concise in your responses.
        """

    @reactive.calc
    def agent():
        req(selected_provider(), selected_model())

        # Create new agent with selected provider and model
        new_agent = chatlas.ChatAuto(
            provider=selected_provider(),
            model=selected_model(),
            system_prompt=system_prompt(),
        )

        # Restore chat history if available
        if chat_history.get():
            new_agent.set_turns(chat_history.get())

        return new_agent

    chat = ui.Chat(id="chat")

    @chat.on_user_submit
    async def chat_ui_respond(user_input: str):
        req(agent())
        
        # Save current chat history before processing new message
        current_turns = agent().get_turns()
        if current_turns:
            chat_history.set(current_turns)
        
        response = await agent().stream_async(user_input)
        await chat.append_message_stream(response)
        
        # Update chat history after processing the message
        updated_turns = agent().get_turns()
        chat_history.set(updated_turns)


app = App(
    app_ui,
    app_server,
    static_assets={"/": www_dir},
)
app.on_shutdown(lambda: www_tempdir.cleanup())
