import chatlas
from shiny import module, reactive, render, req, ui

from tjbots.config import PackageConfig


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
    # Setup environment variables from config - happens automatically on instantiation
    PackageConfig()

    @reactive.calc
    def available_models():
        provider = input.selected_model_provider()
        req(provider)  # Require provider to be truthy

        # Try to get models from API - no fallbacks
        chat_instance = chatlas.ChatAuto(provider=provider)
        models_list = chat_instance.list_models()
        # Convert list of dicts to choices dict: {id: name}
        return {model["id"]: model.get("name", model["id"]) for model in models_list}

    @render.ui
    def model_selector():
        models = available_models()
        req(models)  # Require models to be truthy

        # Select first model as default
        default_model = list(models.keys())[0] if models else None

        return ui.input_select(
            id="selected_model", label="Model", choices=models, selected=default_model
        )  # Return reactive values for use in main app

    return {
        "provider": reactive.calc(lambda: input.selected_model_provider()),
        "model": reactive.calc(
            lambda: getattr(input, "selected_model", lambda: None)()
        ),
    }
