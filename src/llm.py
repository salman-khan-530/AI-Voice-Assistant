import os

from dotenv import load_dotenv
from groq import Groq

# load variable from .env
load_dotenv()

# get groq API key
api_key = os.getenv("GROQ_API_KEY")

# create groq clint
client = Groq(api_key=api_key)

# store conversation history
conversation_history = []

# SYSTEM instruction
SYSTEM_PROMPT = (
    "You are a helpful AI voice assistant. "
    "Give clear and concise answer. "
    "Keep responses suitable for spoken conversation."
)


def generate_response(user_text):
    # send user text to gorq while maintaining conversation history
    # Add user messages to history
    conversation_history.append(
        {
            "role": "user",
            "content": user_text
        }
    )

    # create message for api
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


    # add conversation history
    messages.extend(conversation_history)

    # send request to groq
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )
    except Exception as e:
        print(f"LLM error: {e}")
        conversation_history.pop()
        return None

    # get ai response
    ai_response = response.choices[0].message.content

    # store ai response
    conversation_history.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    return ai_response


if __name__ == "__main__":

    response = generate_response("What is Python?")
    
    print("AI Response:")
    print(response)

    response = generate_response("Who created it?")

    print("\nAI Response:")
    print(response)