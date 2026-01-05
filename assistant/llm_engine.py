import google.generativeai as genai

class LLMEngine:
    """
    Handles communication with Gemini
    """

    def __init__(self, settings):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
