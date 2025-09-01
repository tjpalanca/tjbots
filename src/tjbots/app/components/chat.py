import chatlas
from shiny import module, reactive, req, ui


@module.ui
def chat_ui():
    """Chat UI module.

    Returns a namespaced chat UI. The module is intended to be called as
    ``chat_ui("chat")`` from the application UI.
    """
    return ui.chat_ui(id="chat")


@module.server
def chat_server(input, output, session, selected_provider, selected_model, context):
    """Server side for the chat module.

    This module encapsulates the system prompt and agent creation logic so the
    chat-related reactives live with the chat handlers instead of in the main
    application server. Behavior is unchanged.

    Args:
        selected_provider: reactive that returns the currently-selected provider.
        selected_model: reactive that returns the currently-selected model.
        context: object with a ``turns`` attribute used to retain chat history.
    """

    @reactive.calc
    def current_system_prompt():
        """Return the current system prompt for the agent.

        Returns:
            str: The system prompt text.
        """
        return """
            You are TJBot, a helpful AI assistant created by TJ.
            You are knowledgeable, friendly, and concise in your responses.
        """

    @reactive.calc
    def current_agent():
        """Create and return a chat agent configured with the current selections.

        The agent has retained turns restored from ``context.turns`` so history
        persists even when model/provider selections change.

        Returns:
            chatlas.ChatAuto: the configured chat agent.
        """
        req(selected_provider(), selected_model(), current_system_prompt())

        agent = chatlas.ChatAuto(
            provider=selected_provider(),
            model=selected_model(),
            system_prompt=current_system_prompt(),
        )
        agent.set_turns(context.turns)
        return agent

    chat_ui_obj = ui.Chat(id="chat")

    @chat_ui_obj.on_user_submit
    async def _on_user_submit(user_input: str):
        agent = current_agent()
        response = await agent.stream_async(user_input)
        streamed = await chat_ui_obj.append_message_stream(response)

        @reactive.effect
        @reactive.event(streamed.result)
        def _on_streamed():
            # update retained turns on completion of the streamed response
            context.turns = agent.get_turns()

    # module server is side-effecting; no explicit return required
