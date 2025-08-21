from pathlib import Path

from chatlas import ChatAnthropic
from shiny import App, Inputs, Outputs, Session, ui

from tjbots.config import PackageConfig

config = PackageConfig()

app_dir = Path(__file__).parent
www_dir = app_dir / "www"
assets_dir = app_dir.parent.parent.parent / "assets"

tjbots_icon = ui.img(style="background-color: white;", src="assets/logo/tjbots.svg")
app_ui = ui.page_sidebar(
    ui.sidebar(ui.input_dark_mode(), open="closed"),
    # Progressive Web App
    ui.head_content(
        ui.tags.link(rel="stylesheet", href="custom.css"),
        ui.tags.link(rel="manifest", href="manifest.json"),
        ui.tags.link(
            rel="icon",
            type="image/svg+xml",
            size="any",
            href="assets/logo/tjbots.svg",
        ),
        ui.tags.link(
            rel="shortcut icon",
            type="image/svg+xml",
            size="any",
            href="assets/logo/tjbots.svg",
        ),
        ui.tags.link(rel="apple-touch-icon", href="assets/logo/tjbots.png"),
        ui.tags.meta(
            name="viewport",
            content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover",
        ),
        ui.tags.meta(name="mobile-web-app-capable", content="yes"),
        ui.tags.meta(name="apple-mobile-web-app-status-bar-style", content="default"),
        ui.tags.script("""
        $(document).on('shiny:connected', function() {
            if (window.Shiny && Shiny.shinyapp) Shiny.shinyapp.$allowReconnect = true;
        });
        """),
    ),
    # Chat Contents
    ui.chat_ui(id="chat", icon_assistant=tjbots_icon),
    # Other Settings
    window_title="TJBots",
    fillable=True,
    fillable_mobile=True,
)


def app_server(input: Inputs, output: Outputs, session: Session):
    chat_ui = ui.Chat(id="chat")
    assert config.anthropic_api_key
    chat = ChatAnthropic(
        model="claude-opus-4-1-20250805",
        system_prompt="""
            You are TJBot, a helpful AI assistant created by TJ.
            You are knowledgeable, friendly, and concise in your responses.
        """,
        api_key=config.anthropic_api_key.get_secret_value(),
    )

    @chat_ui.on_user_submit
    async def chat_ui_respond(user_input: str):
        response = await chat.stream_async(user_input)
        await chat_ui.append_message_stream(response)


app = App(
    app_ui,
    app_server,
    static_assets={"/": www_dir, "/assets": assets_dir},
)
