class FridayAssistant:
    """
    Orchestrates the interaction between:
    - Memory
    - PromptController
    - LLMEngine
    """

    def __init__(
        self,
        llm_engine,
        prompt_controller,
        memory
    ):
        self.llm_engine = llm_engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def respond(self, user_input: str, role: str) -> str:
        """
        Main assistant workflow:
        1. Load conversation memory
        2. Build prompt
        3. Generate response
        4. Save interaction
        5. Return response
        """

        history_text = self.memory.get_history()

        prompt = self.prompt_controller.build_prompt(
            role=role,
            memory_text=history_text,
            user_input=user_input
        )

        assistant_reply = self.llm_engine.generate(prompt)

        self.memory.add("user", user_input)
        self.memory.add("assistant", assistant_reply)

        return assistant_reply
