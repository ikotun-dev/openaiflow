import os

import dotenv
import openai

# import time
dotenv.load_dotenv()


class OpenaiWrapper:
    def __init__(self, api_key):
        self._api_key = api_key  # set to protected
        openai.api_key = self._api_key
        self.client = None

    def validate_api_key(self):
        try:
            client = openai.OpenAI()
            # testing validity of the api_key by creating a message
            _ = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Can you read this?"},
                ],
            )

            print("API key is valid")
        except Exception as e:
            print(f"Error : {e}")
            print("API key is invalid")


client = OpenaiWrapper(os.getenv("KEY"))
client.validate_api_key()
