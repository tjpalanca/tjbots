"""
Minimal test app for testing the sidebar component.
"""

from shiny import App, render, ui

from tjbots.app.components.sidebar import sidebar_server, sidebar_ui

app_ui = ui.page_sidebar(
    sidebar_ui("sidebar"),
    ui.output_text("selected_provider_text"),
    ui.output_text("selected_model_text"),
)


def server(input, output, session):
    selected_provider, selected_model = sidebar_server("sidebar")

    @render.text
    def selected_provider_text():
        return f"Provider: {selected_provider()}"

    @render.text
    def selected_model_text():
        return f"Model: {selected_model()}"


app = App(app_ui, server)
