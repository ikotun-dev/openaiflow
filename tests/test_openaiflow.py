import unittest
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

        self.wrapper.client = MagicMock()

    def test_validate_api_key(self):
        with self.assertRaises(ValueError):
            invalid_client = api.OpenaiWrapper("")
            invalid_client.validate_api_key()

    def test_create_assistant_success(self):
        self.wrapper.client.beta.assistants.create.return_value = {
            "id": "test_assissant_id"
        }
        name = "TestModel"
        instructions = "Test instructions"
        model = "gpt-3.5-turbo"

        assistant = self.wrapper.client.create_assistant(name, instructions, model)
        self.assertIsNotNone(assistant)

    def test_creating_thread_with_invalid_data(self):
        with self.assertRaises(ValueError):
            invalid_client = api.OpenaiWrapper("")
            invalid_client.create_thread("")

    def test_create_assistant_missing_total_data(self):
        with self.assertRaises(ValueError):
            invalid_client = api.OpenaiWrapper("")
            invalid_client.create_assistant("", "", "")
