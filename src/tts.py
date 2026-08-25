from google import genai
from dotenv import load_dotenv
import os
import base64
import wave

load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

# Create Gemini client
client = genai.Client(api_key=api_key)


def save_wave_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Save raw PCM audio data as a WAV file."""

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)


def text_to_speech(text, output_file="response.wav"):
    """
    Convert text into speech using Gemini TTS.
    """

    try:
        response = client.interactions.create(
            model="gemini-2.5-flash-preview-tts",
            input=f"Say naturally and clearly: {text}",
            response_format={"type": "audio"},
            generation_config={
                "speech_config": [
                    {
                        "voice": "Kore"
                    }
                ]
            }
        )

        # Get generated audio
        audio_data = base64.b64decode(
            response.output_audio.data
        )

        # Save as WAV
        save_wave_file(
            output_file,
            audio_data
        )

        return output_file

    except Exception as e:
        print(f"TTS Error: {e}")
        return None