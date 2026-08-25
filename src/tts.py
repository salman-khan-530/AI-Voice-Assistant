from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def text_to_speech(text, output_file="response.wav"):
    """
    Convert text into speech using Groq TTS.
    """

    try:
        response = client.audio.speech.create(
            model="canopylabs/orpheus-v1-english",
            voice="troy",
            input=text,
            response_format="wav"
        )

        response.write_to_file(output_file)

        return output_file

    except Exception as e:
        print(f"TTS Error: {e}")
        return None