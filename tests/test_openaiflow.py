import unittest
import openai
from unittest.mock import MagicMock
from openaiflow import api
import os
import dotenv

dotenv.load_dotenv()


class TestOpenAIFlow(unittest.TestCase):
    def setUp(self):
        """This method is called before each test"""
        api_key = os.getenv("OPENAI_API_KEY")
        self.wrapper = api.OpenaiWrapper(api_key)

        assert self.wrapper._api_key == api_key
        assert self.wrapper.headers["Authorization"] == f"Bearer {api_key}"
        assert self.wrapper.headers["Content-Type"] == "application/json"
        assert self.wrapper.headers["OpenAI-Beta"] == "assistants=v2"

    def test_validate_api_key(self):
        with self.assertRaises(ValueError):
            invalid_client = api.OpenaiWrapper("")
            invalid_client.validate_api_key()

    def test_create_assistant_success(self):
        self.wrapper.client = MagicMock()

        self.wrapper.client.beta.assistants.create.return_value = {
            "id": "test_assissant_id"
        }
        name = "TestModel"
        instructions = "Test instructions"
        model = "gpt-3.5-turbo"

        assistant = self.wrapper.client.create_assistant(name, instructions, model)
        self.assertIsNotNone(assistant)

    def test_creating_thread_with_empty_data(self):
        with self.assertRaises(ValueError):
            invalid_client = api.OpenaiWrapper("")
            invalid_client.create_thread("")

    def test_validate_thread_with_invalid_data(self):
        result = self.wrapper.validate_thread("fake_thread")
        self.assertIsNone(result)

    def test_create_assistant_missing_total_data(self):
        with self.assertRaises(ValueError):
            invalid_client = api.OpenaiWrapper("")
            invalid_client.create_assistant("", "", "")

    def test_validate_assistant_with_invalid_data(self):
        result = self.wrapper.validate_assistant("fake_assistant")
        self.assertIsNone(result)

    def test_interactive_chat_with_empty_message(self):
        with self.assertRaises(ValueError):
            self.wrapper.interactive_chat(
                "thread_Wj0bl4180TUbdGXZC8vPkpFk", "asst_LrftItf8EYHpwKQlVsgWih2g", None
            )
