import os

import dotenv
import openai

# import time
dotenv.load_dotenv()

# TODO: Add a method to check the validity of the api
# TODO: create assistant
# TODO: create a thread
# TODO: store messages ( in memory ) for a thread


"""
MESSAGES_URL = (
    f"https://api.openai.com/v1/threads/{thread_id}/messages?limit=1&order=desc"
)
"""


class OpenaiWrapper:
    def __init__(self, api_key):
        self._api_key = api_key  # set to protected
        openai.api_key = self._api_key
        self.client = None

        self.headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2",
        }

    def validate_api_key(self):
        """
        tests validity of the api_key by creating a message
        """
        try:
            client = openai.OpenAI()
            _ = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Can you read this?"},
                ],
            )

            print(_.choices[0])
            print("API key is valid")
        except Exception as e:
            print(f"Error : {e}")
            print("API key is invalid")

    def create_assistant(self):
        pass


# client = OpenaiWrapper(os.getenv("KEY"))
client = OpenaiWrapper("ah")
client.validate_api_key()
