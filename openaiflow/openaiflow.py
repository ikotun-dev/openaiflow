import os
import time

import dotenv
import openai
import requests
from openai import OpenAI

from . import file_parser

dotenv.load_dotenv()


class OpenaiWrapper:
    def __init__(self, api_key):
        self._api_key = api_key
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
            _ = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Can you read this?"},
                ],
            )

            return True
        except openai.AuthenticationError:
            raise ValueError("API key is invalid")

        except Exception as e:
            raise ValueError(f"An error occured : {e}")

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

        except openai.NotFoundError:
            return None

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

        except openai.NotFoundError:
            return None
        except openai.BadRequestError as e:
            raise ValueError(f"Error validating thread: {e}")

    def create_run(self, thread_id, assistant_id):
        try:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=assistant_id
            )
            return run
        except Exception as e:
            raise ValueError(f"Error creating run: {e}")

    def retrieve_run(self, thread_id, run_id):
        try:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
            return run
        except Exception as e:
            raise ValueError(f"Error retrieving run: {e}")

    def get_latest_messages(self, thread_id):
        try:
            MESSAGES_URL = f"https://api.openai.com/v1/threads/{thread_id}/messages?limit=1&order=desc"

            previous_messages = requests.get(MESSAGES_URL, headers=self.headers)
            if previous_messages.status_code != 200:
                raise ValueError("Error fetching messages")
            return previous_messages.json()

        except Exception as e:
            raise ValueError(f"Error fetching messages: {e}")
            pass

    def chat(self, input_type, **kwargs):
        """
        This is the main method to chat with the assistant,
        various input formats would be supported, one time messaging, and a back and forth mechanism.

        :param input_type: str -> type of input to be used (console, interactive). Default is console
        """
        # NOTE: user to pass thread_id=None -> if they need to create new thread

        required_keys = ["assistant_id", "thread_id"]

        for key in required_keys:
            if key not in kwargs:
                raise ValueError(f"Missing required key: {key}")

        _assistant = self.validate_assistant(kwargs["assistant_id"])

        # NOTE: can handle this anyhow you want :- in memory, db, etc.
        if kwargs["thread_id"] is not None:
            thread = self.validate_thread(kwargs["thread_id"])
            messages = self.get_latest_messages(kwargs["thread_id"])
            print(messages)

        if kwargs["thread_id"] is None:
            thread = self.create_thread(kwargs["assistant_id"])
            kwargs["thread_id"] = thread.id

        if input_type == "console":
            self.console_chat(kwargs["thread_id"], kwargs["assistant_id"], messages)

    def console_chat(self, thread_id, assistant_id, messages):
        """
        This method is used to chat with the assistant via the console
        """
        try:
            new_run = self.create_run(thread_id, assistant_id)

            while True:
                user_message = input("You: ")
                if user_message == "exit":
                    break
                assistant_response, _, _ = self.handle_message(
                    user_message, thread_id, assistant_id, new_run.id
                )
                print(f"Assistant: {assistant_response}")
        except Exception as e:
            raise ValueError(f"Error chatting with assistant: {e}")

    def handle_message(self, message, thread_id, assistant_id, run_id=None):
        """
        This method is used to handle messages to and from the assistant

        :param message: str -> The message to be sent to the assistant_id
        :param thread_id: str -> The thread_id to be used
        :param assistant_id: str -> The assistant_id to be used
        """

        _messages = self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message
        )

        # NOTE: can handle this anyhow you want :- in memory, db, etc

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )

        print("Run ID : ", run.id)
        run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        time.sleep(0.5)
        print(f"STATUS : {run.status} ✅")

        while run.status in ["in_progress", "queued"]:
            print("Waiting for response...")
            # TODO: make users set their own time
            time.sleep(5)
            run = self.retrieve_run(thread_id, run.id)

        # the response just provided by the bot
        previous_message = self.get_latest_messages(thread_id)
        parsed_response = self.parse_assistant_response(previous_message)

        return parsed_response

    def interactive_chat(self, thread_id, assistant_id, message=None):
        """
        This method is used to chat with the assistant interactively
        passing message back and forth from & to the assistant
        """
        try:
            if message is None:
                raise ValueError("Message provided should not be empty")

            thread = self.validate_thread(thread_id)

            if thread is None:
                thread = self.create_thread(assistant_id)
                print("Thread created successfully")
            else:
                print("Thread retrevied successfully.")

            # new_run = self.create_run(thread_id, assistant_id)

            assistant = self.validate_assistant(assistant_id)
            if assistant is None:
                print("Assistant not found")
                return

            assistant_response = self.handle_message(
                message,
                thread_id,
                assistant_id,
            )
            return assistant_response

            pass
        except openai.AuthenticationError as e:
            raise ValueError(f"Error authenticating: {e}")

    def parse_assistant_response(self, response):
        """
        Parse the assistant response to extract relevant information.

        :param response: dict -> The response from the assistant.
        :return: Tuple[str, str, str] -> Assistant's message, thread_id, run_id
        """

        if "data" in response and response["data"]:
            latest_message = response["data"][-1]
            assistant_message = (
                latest_message["content"][0]["text"]["value"]
                if latest_message["content"]
                else "No content available"
            )

            thread_id = latest_message["thread_id"]
            run_id = latest_message["run_id"]

            return assistant_message, thread_id, run_id
        else:
            return "No messages found", None, None
