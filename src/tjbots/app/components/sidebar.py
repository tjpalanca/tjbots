from shiny import module, ui


@module.ui
def sidebar_ui():
    return ui.sidebar(
        ui.input_select(
            id="selected_model_provider",
            label="Model Provider",
            choices={"anthropic": "Anthropic", "google": "Google", "openai": "OpenAI"},
        ),
        ui.output_ui("model_selector"),
        open="desktop",
    )


@module.server
def sidebar_server(input, output, session):
    pass
