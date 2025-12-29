
import os
from dotenv import load_dotenv


class Settings:
    """
    application configuration.
    loads and validates environment variables.
    """

    def __init__(self):
        load_dotenv()
        self.gemini_api_key = self._load_gemini_key()

    def _load_gemini_key(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Please set it in your .env file."
            )

        return api_key


# settings = Settings()
# print(settings.gemini_api_key)
