class PromptController:
    def __init__(self):
        pass

    def build_prompt(self, role, memory_text, user_input):

        """
        Builds a structured prompt for the Friday AI assistant.

        This method combines:
        - System-level assistant identity
        - Selected assistant role (Tutor, Coder, Mentor)
        - Previous conversation memory
        - Current user input

        The final prompt is formatted so the AI responds consistently as "Friday".
        """
        
        prompt = f"You are Friday, a personal AI assistant.\n"
        prompt += f"Your role is: {role}\n\n"

        prompt += "Conversation so far:\n"
        prompt += memory_text + "\n"

        prompt += "User says:\n"
        prompt += user_input + "\n\n"

        prompt += "Friday:"
        return prompt



