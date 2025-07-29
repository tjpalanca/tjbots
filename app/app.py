import os

from pathlib import Path
from chatlas import ChatOpenAI
from dotenv import load_dotenv
from shiny import App, Inputs, Outputs, Session, ui

load_dotenv()

app_ui = ui.page_sidebar(
    ui.sidebar(open="closed"),
    ui.chat_ui(id="chat", icon_assistant=ui.img(src="assets/images/tjbots.svg")),
    ui.head_content(ui.tags.meta(rel="manifest", href="manifest.json")),
    fillable=True,
    fillable_mobile=True
)


def server(input: Inputs, output: Outputs, session: Session):

    chat_ui = ui.Chat(id="chat")
    chat = ChatOpenAI(
        model="gpt-4o-mini",
        system_prompt="""
            You are TJBot, a helpful AI assistant created by TJ.
            You are knowledgeable, friendly, and concise in your responses.
        """,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    @chat_ui.on_user_submit
    async def chat_ui_respond(user_input: str):
        response = await chat.stream_async(user_input)
        await chat_ui.append_message_stream(response)

app_dir = Path(__file__).parent
app = App(app_ui, server, static_assets={
    "/assets": app_dir.parent / "assets",
    "/manifest.json": app_dir / "manifest.json"
})
