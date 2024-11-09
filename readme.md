### OpenAIFlow

<br/>
OpenAIFlow is a Python library designed to simplify interactions with the OpenAI API, allowing you to create and manage assistants, threads, and messaging workflows effortlessly.

Features

- Validate and manage OpenAI API keys
- Create and manage custom assistants
- Create assistants with files
- Start new threads for conversations with assistants
- Chat in different formats (console, interactive)
- Retrieve and parse the latest assistant responses
- Installation

To install the library, run:

```bash
pip install openaiflow
```

### Getting Started

#### 1. Setup

Set up your OpenAI API key:
Create a .env file in your project directory and add your OpenAI API key:

```js
KEY = `your_openai_api_key`;
```

Alternatively, you can pass the API key directly [this is not a good practice] when initializing OpenAIWrapper.

#### 2. Initialize OpenAIWrapper:

```python
from openaiflow import openaiflow
import os

# Load API key from environment
api_key = os.getenv("KEY")
client = openaiflow.OpenAIWrapper(api_key)
```

#### 3. Validating Your API Key

```python
if client.validate_api_key():
	print("API key is valid.")
else:
	print("Invalid API key.")
```

> Your OpenAI client is now up and running.

#### 4. Creating an Assistant

An _assistant_ is a configured AI persona, defined by its name, instructions (like tone and purpose), and model (e.g., `gpt-3.5-turbo`). Different assistants can be tailored for specific tasks like support, creativity, or information.

You can create a custom assistant by providing a name, instructions, and model type:

```python
assistant = client.create_assistant(
name="Test Assistant",
instructions="You are a helpful assistant.",
model="gpt-3.5-turbo"
)
```

#### 5. Starting a New Thread

A thread is a session-based conversation with an assistant, maintaining context across messages in that session. Multiple threads can be created with the same assistant, each handling different topics or interactions independently.

A thread is used to initiate a conversation with the assistant:

```python
thread = client.create_thread(assistant_id="your_assistant_id")
```

#### 6. Interactive Chat

> Use the interactive_chat function for a back-and-forth conversation with the assistant:

```python
response = client.interactive_chat(
thread_id="your_thread_id",
assistant_id="your_assistant_id",
message="Hello, how can you help me?"
)
print("Assistant:", response)
```

> A very basic usage on `interactive_chat`

```python
key = True # flag to show an ongoing conversation
while key:
	user_input = input() # this input can come in any form

    response = client.interactive_chat(
		thread_id="your_thread_id",
		assistant_id="your_assistant_id",
		message="Hello, how can you help me?"
	)
    print(f"Assistant Response: {response}")
```

#### 4. Console Chat

For a console-based chat where you can type messages directly:

```python
client.chat(
input_type="console",
assistant_id="your_assistant_id",
thread_id="your_thread_id"
)
```

Type exit to end the chat session.

#### 5. Handling Messages

OpenAIFlow also allows you to handle incoming and outgoing messages in your threads. For example:

```python
response, thread_id, run_id = client.handle_message(
message="What can you do?",
thread_id="your_thread_id",
assistant_id="your_assistant_id"
)

print("Assistant:", response)
```

#### 6. Parsing Responses

If you need to parse a response from the assistant:

```python
parsed_response = client.parse_assistant_response(response)
print("Assistant says:", parsed_response[0])
```

#### 7. Error Handling

OpenAIFlow includes structured error handling, so you can handle issues with API keys, message failures, and more.

Example:

```python
try:
	client.create_thread("invalid_id")
except ValueError as e:
	print(e) # Outputs error message
```

#### TODOs & Future Improvements

- Allow customization of model parameters
- Add adjustable sleep intervals for response polling
- Add image support
- Add streaming support
- Store messages in memory for easy retrieval and context switching

#### License

This project is licensed under the MIT License.
