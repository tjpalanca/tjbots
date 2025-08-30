from pathlib import Path
from tempfile import TemporaryDirectory

from chatlas import ChatAnthropic
from shiny import App, Inputs, Outputs, Session, ui

from tjbots.app.modules.pwa import pwa_ui
from tjbots.app.modules.reconnect import reconnect_ui
from tjbots.config import PackageConfig

config = PackageConfig()

app_dir = Path(__file__).parent
www_tempdir = TemporaryDirectory("tjbots_app_www")
www_dir = Path(www_tempdir.name)
assets_dir = app_dir.parent.parent.parent / "assets"


app_ui = ui.page_sidebar(
    ui.sidebar(ui.input_dark_mode(), open="closed"),
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
    static_assets={"/": www_dir},
)
app.on_shutdown(lambda: www_tempdir.cleanup())
