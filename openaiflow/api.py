import os
import requests
import dotenv
import file_parser
from openai import OpenAI

# import time
dotenv.load_dotenv()

# TODO: Add a method to check the validity of the api
# TODO: create assistant
# TODO: create a thread
# TODO: store messages ( in memory ) for a thread


class OpenaiWrapper:
    def __init__(self, api_key):
        self._api_key = api_key  # set to protected
        self.client = OpenAI(api_key=self._api_key)

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
            # self.client = openai.OpenAI()
            _ = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Can you read this?"},
                ],
            )

            # print(_.choices[0])
            return True
        except Exception as e:
            raise ValueError(f"API key is invalid : {e}")

    def create_assistant(self, name, instructions, model):
        try:
            if not name or not instructions or not model:
                raise ValueError("Name, instructions and model are required")

            assistant = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model,
                tools=[{"type": "code_interpreter"}],
            )
            return assistant
        except Exception as e:
            raise ValueError(f"Error creating assistant: {e}")

    def validate_assistant(self, assistant_id):
        try:
            assistant = self.client.beta.assistants.retrieve(assistant_id)
            return assistant
        except Exception as e:
            raise ValueError(f"Error validating assistant: {e}")

    def create_assistant_via_file(self, name, model, file):
        try:
            instructions = file_parser.extract_text_from_file(file)
            return self.create_assistant(name, instructions, model)
        except ValueError:
            raise ValueError("Error extracting text from file")

    def create_thread(self, assistant_id):
        try:
            thread = self.client.beta.threads.create()
            return thread
        except Exception as e:
            raise ValueError(f"Error creating thread: {e}")

    def validate_thread(self, thread_id):
        try:
            thread = self.client.beta.threads.retrieve(thread_id)
            return thread
        except Exception as e:
            raise ValueError(f"Error validating thread: {e}")

    def get_latest_messages(self, thread_id):
        try:
            MESSAGES_URL = f"https://api.openai.com/v1/threads/{thread_id}/messages?limit=10&order=desc"

            previous_messages = requests.get(MESSAGES_URL, headers=self.headers)
            if previous_messages.status_code != 200:
                raise ValueError("Error fetching messages")
            return previous_messages.json()

        except Exception as e:
            raise ValueError(f"Error fetching messages: {e}")
            pass

    def chat(self, **kwargs):
        # user to pass thread_id=None -> if they need to create new thread

        required_keys = ["assistant_id", "thread_id"]

        for key in required_keys:
            if key not in kwargs:
                raise ValueError(f"Missing required key: {key}")

        # validate assistant
        _assistant = self.validate_assistant(kwargs["assistant_id"])

        # can handle this anyhow you want :- in memory, db, etc.
        if kwargs["thread_id"] is not None:
            thread = self.validate_thread(kwargs["thread_id"])
            # get latest messages
            messages = self.get_latest_messages(kwargs["thread_id"])
            print(messages)

        if kwargs["thread_id"] is None:
            thread = self.create_thread(kwargs["assistant_id"])
            kwargs["thread_id"] = thread.id

        # if everything has been validated, we can now chat
        print("Chatting....")
        user_message = input("You: ")

    def chat_console():
        """
        This function enables chatting  with the assistant via the console
        """
        pass

    def chat_websocket(self, websocket, **kwargs):
        pass


client = OpenaiWrapper(os.getenv("KEY"))
client.validate_api_key()


#
# print(client.get_latest_messages("thread_DMrqTY8eLuHxh97T60jgy3GR"))
client.chat(thread_id=None, assistant_id="ass_234")
