OpenAIFlow
<br/>
OpenAIFlow is a Python library designed to simplify interactions with the OpenAI API, allowing you to create and manage assistants, threads, and messaging workflows effortlessly.

Features

- Validate and manage OpenAI API keys
- Create and manage custom assistants
- Start new threads for conversations with assistants
- Chat in different formats (console, interactive)
- Retrieve and parse the latest assistant responses
- Installation

To install the library, run:

bash```
pip install openaiflow

```


### Getting Started
Setup
Set up your OpenAI API key:

Create a .env file in your project directory and add your OpenAI API key:
makefile
Copy code
KEY=your_openai_api_key
Alternatively, you can pass the API key directly when initializing OpenAIWrapper.
Initialize OpenAIWrapper:

python
Copy code
from openaiflow import OpenAIWrapper
import os

# Load API key from environment

api_key = os.getenv("KEY")
client = OpenAIWrapper(api_key)
Validating Your API Key
Check if your API key is valid:

python
Copy code
if client.validate_api_key():
print("API key is valid.")
else:
print("Invalid API key.")
Creating an Assistant
You can create a custom assistant by providing a name, instructions, and model type:

python
Copy code
assistant = client.create_assistant(
name="Test Assistant",
instructions="You are a helpful assistant.",
model="gpt-3.5-turbo"
)
print(assistant)
Starting a New Thread
Create a thread to initiate a conversation with the assistant:

python
Copy code
thread = client.create_thread(assistant_id="your_assistant_id")
print(thread.id)
Interactive Chat
Use the interactive_chat function for a back-and-forth conversation with the assistant:

python
Copy code
response = client.interactive_chat(
thread_id="your_thread_id",
assistant_id="your_assistant_id",
message="Hello, how can you help me?"
)
print("Assistant:", response)
Console Chat
For a console-based chat where you can type messages directly:

python
Copy code
client.chat(
input_type="console",
assistant_id="your_assistant_id",
thread_id="your_thread_id"
)
Type exit to end the chat session.

Handling Messages
OpenAIFlow also allows you to handle incoming and outgoing messages in your threads. For example:

python
Copy code
response, thread_id, run_id = client.handle_message(
message="What can you do?",
thread_id="your_thread_id",
assistant_id="your_assistant_id"
)
print("Assistant:", response)
Parsing Responses
If you need to parse a response from the assistant:

python
Copy code
parsed_response = client.parse_assistant_response(response)
print("Assistant says:", parsed_response[0])
Error Handling
OpenAIFlow includes structured error handling, so you can handle issues with API keys, message failures, and more.

Example:

python
Copy code
try:
client.create_thread("invalid_id")
except ValueError as e:
print(e) # Outputs error message
TODOs & Future Improvements
Allow customization of model parameters
Add adjustable sleep intervals for response polling
Store messages in memory for easy retrieval and context switching
License
This project is licensed under the MIT License.
```
