import os
from pathlib import Path

from chatlas import ChatOpenAI
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, ui

load_dotenv()

app_dir = Path(__file__).parent

# icon used for assistant messages
tjbots_icon = ui.img(style="background-color: white;", src="assets/images/tjbots.svg")

# Application UI using Framework7 styles
app_ui = ui.tags.html(
    ui.tags.head(
        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/framework7@8.3.2/framework7-bundle.min.css",
        ),
        ui.include_css(app_dir / "custom.css"),
        ui.tags.link(rel="manifest", href="manifest.json"),
        ui.tags.link(rel="apple-touch-icon", href="assets/images/tjbots.png"),
        ui.tags.meta(
            name="viewport",
            content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover",
        ),
        ui.tags.script(src="https://cdn.jsdelivr.net/npm/framework7@8.3.2/framework7-bundle.min.js"),
    ),
    ui.tags.body(
        {"class": "framework7-root"},
        ui.tags.div(
            {"id": "app"},
            ui.tags.div(
                {"class": "view view-main"},
                ui.tags.div(
                    {"class": "page"},
                    ui.tags.div(
                        {"class": "page-content"},
                        ui.chat_ui(
                            id="chat",
                            icon_assistant=tjbots_icon,
                        ),
                    ),
                ),
            ),
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    chat_ui = ui.Chat(id="chat")
    chat = ChatOpenAI(
        model="gpt-4o-mini",
        system_prompt="""
            You are TJBot, a helpful AI assistant created by TJ.
            You are knowledgeable, friendly, and concise in your responses.
        """,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    @chat_ui.on_user_submit
    async def chat_ui_respond(user_input: str):
        response = await chat.stream_async(user_input)
        await chat_ui.append_message_stream(response)


app = App(
    app_ui,
    server,
    static_assets={
        "/assets": app_dir.parent / "assets",
        "/manifest.json": app_dir / "manifest.json",
    },
)
