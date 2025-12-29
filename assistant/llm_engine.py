
import google.generativeai as genai


class LLMEngine:
    """
    Handles interaction with the LLM (Gemini).
    Input: prompt (str)
    Output: generated text (str)
    """

    def __init__(self, settings):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text


