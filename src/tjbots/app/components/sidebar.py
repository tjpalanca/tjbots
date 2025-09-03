from shiny import module, render, req, ui

MODEL_PROVIDER_CHOICES = {
    "anthropic": "Anthropic",
    "google": "Google",
    "openai": "OpenAI",
}

MODEL_CHOICES = {
    "anthropic": {
        "default": "claude-sonnet-4-20250514",
        "choices": {
            "claude-opus-4-1-20250805": "Claude Opus 4.1",
            "claude-sonnet-4-20250514": "Claude Sonnet 4",
            "claude-opus-4-20250514": "Claude Opus 4",
            "claude-3-opus-20240229": "Claude Opus 3",
            "claude-3-7-sonnet-20250219": "Claude Sonnet 3.7",
            "claude-3-5-sonnet-20241022": "Claude Sonnet 3.5",
            "claude-3-5-haiku-20241022": "Claude Haiku 3.5",
            "claude-3-haiku-20240307": "Claude Haiku 3",
        },
    },
    "google": {
        "default": "gemini-2.5-flash",
        "choices": {
            "gemini-2.5-pro": "Gemini 2.5 Pro",
            "gemini-2.5-flash": "Gemini 2.5 Flash",
            "gemini-2.5-flash-lite": "Gemini 2.5 Flash Lite",
            "gemini-2.0-flash": "Gemini 2.0 Flash",
            "gemini-2.0-flash-lite": "Gemini 2.0 Flash Lite",
            "gemini-1.5-pro": "Gemini 1.5 Pro",
            "gemini-1.5-flash": "Gemini 1.5 Flash",
        },
    },
    "openai": {
        "default": "gpt-5-mini",
        "choices": {
            "gpt-5": "GPT-5",
            "gpt-5-mini": "GPT-5 mini",
            "gpt-5-nano": "GPT-5 nano",
            "gpt-4.1": "GPT 4.1",
            "gpt-4.1-mini": "GPT 4.1 mini",
            "gpt-4.1-nano": "GPT 4.1 nano",
        },
    },
}


@module.ui
def sidebar_ui():
    return ui.sidebar(
        ui.input_select(
            id="selected_provider",
            label="Model Provider",
            choices=MODEL_PROVIDER_CHOICES,
        ),
        ui.output_ui("model_selector"),
        open="desktop",
    )


@module.server
def sidebar_server(input, output, session):
    @render.ui
    def model_selector():
        req(input.selected_provider())
        model_choices = MODEL_CHOICES[input.selected_provider()]

        return ui.input_select(
            id="selected_model",
            label="Model",
            choices=model_choices["choices"],
            selected=model_choices["default"],
        )

    return (input.selected_provider, input.selected_model)
