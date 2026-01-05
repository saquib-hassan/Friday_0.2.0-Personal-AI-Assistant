class PromptController:
    """
    Builds structured prompts for Friday
    """

    def build_prompt(self, role, memory_text, user_input):
        prompt = f"You are Friday, a personal AI assistant.\n"
        prompt += f"Your role is: {role}\n\n"

        prompt += "Conversation so far:\n"
        prompt += memory_text + "\n"

        prompt += "User says:\n"
        prompt += user_input + "\n\n"

        prompt += "Friday:"
        return prompt
