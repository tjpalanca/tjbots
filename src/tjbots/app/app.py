from pathlib import Path

from chatlas import ChatAnthropic
from shiny import App, Inputs, Outputs, Session, ui

from tjbots.config import PackageConfig
from tjbots.app.ui import pwa_head_content, sidebar, tjbots_icon

config = PackageConfig()

app_dir = Path(__file__).parent
www_dir = app_dir / "www"
assets_dir = app_dir.parent.parent.parent / "assets"


def app_ui(_):
    tjbots_icon_component = tjbots_icon()
    return ui.page_sidebar(
        sidebar(),
        # Progressive Web App
        pwa_head_content(),
        # Reconnection script
        ui.head_content(
            ui.tags.script("""
        $(document).on('shiny:connected', function() {
            if (window.Shiny && Shiny.shinyapp) Shiny.shinyapp.$allowReconnect = true;
        });
        """)
        ),
        # Chat Contents
        ui.chat_ui(id="chat", icon_assistant=tjbots_icon_component),
        # Other Settings
        window_title="TJBots",
        fillable=True,
        fillable_mobile=True,
    )


def app_server(input: Inputs, output: Outputs, session: Session):
    chat = ui.Chat(id="chat")

    agent = ChatAnthropic(
        model="claude-opus-4-1-20250805",
        system_prompt="""
            You are TJBot, a helpful AI assistant created by TJ.
            You are knowledgeable, friendly, and concise in your responses.
        """,
        api_key=(
            config.anthropic_api_key.get_secret_value()
            if config.anthropic_api_key
            else None
        ),
    )

    @chat.on_user_submit
    async def chat_ui_respond(user_input: str):
        response = await agent.stream_async(user_input)
        await chat.append_message_stream(response)


app = App(
    app_ui,
    app_server,
    static_assets={"/": www_dir, "/assets": assets_dir},
)
