class FridayAssistant:
    """
    Orchestrates memory → prompt → LLM → response
    """

    def __init__(self, llm_engine, prompt_controller, memory):
        self.llm_engine = llm_engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def respond(self, user_input, role):
        history = self.memory.get_history()

        prompt = self.prompt_controller.build_prompt(
            role=role,
            memory_text=history,
            user_input=user_input
        )

        reply = self.llm_engine.generate(prompt)

        self.memory.add("user", user_input)
        self.memory.add("assistant", reply)

        return reply
