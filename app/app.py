from shiny import App, Inputs, Outputs, Session, ui

app_ui = ui.page_sidebar(
    ui.sidebar(open="closed"),
    ui.chat_ui(id="chat")
)


def server(input: Inputs, output: Outputs, session: Session):
    pass


app = App(app_ui, server)
