
class FridayAssistant:
    def __init__(self, llm_engine, prompt_controller, memory):
        #dependency injection
        
        self.llm_engine = llm_engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def respond(self, user_input, role):
        """
        steps:
        1. get conversation history from memory
        2. build prompt
        3. generate response from LLM
        4. save user & assistant messages
        5. return assistant response
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
        

