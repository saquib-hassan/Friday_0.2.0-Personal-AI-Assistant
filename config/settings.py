# import os
# from dotenv import load_dotenv


# class Settings:
#     """
#     Application configuration.
#     Loads and validates environment variables.
#     """

#     def __init__(self):
#         load_dotenv()

#         # AI
#         self.gemini_api_key = self._load_gemini_key()

#         # Database
#         self.DB_HOST = self._load_env("DB_HOST")
#         self.DB_USER = self._load_env("DB_USER")
#         self.DB_PASSWORD = self._load_env("DB_PASSWORD")
#         self.DB_NAME = self._load_env("DB_NAME", required=False)

#     def _load_gemini_key(self):
#         api_key = os.getenv("GEMINI_API_KEY")

#         if not api_key:
#             raise RuntimeError(
#                 "GEMINI_API_KEY is missing. "
#                 "Please set it in your .env file."
#             )

#         return api_key

#     def _load_env(self, key, required=True):
#         value = os.getenv(key)

#         if required and not value:
#             raise RuntimeError(f"{key} is missing in .env file")

#         return value

import os
from dotenv import load_dotenv

class Settings:
    """
    Loads and validates environment variables
    """

    def __init__(self):
        load_dotenv()

        self.gemini_api_key = self._get("GEMINI_API_KEY")
        self.db_host = self._get("DB_HOST")
        self.db_user = self._get("DB_USER")
        self.db_password = self._get("DB_PASSWORD")
        self.db_name = self._get("DB_NAME")

    def _get(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise RuntimeError(f"Missing environment variable: {key}")
        return value
