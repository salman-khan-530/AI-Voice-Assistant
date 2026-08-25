from src.audio import record_audio
from src.stt import speech_to_text
from src.llm import generate_response
from src.tts import text_to_speech

AUDIO_FILE = "audio.wav"

EXIT_COMMANDS = ["exit", "stop", "quit"]

def main():

    print("=" * 50)
    print("       AI VOICE ASSISTANT")
    print("=" * 50)

    print("\nSay 'exit', 'stop', or 'quit' to end the assistant.\n")

    while True:
        try:
            # Record user's voice
            recorded = record_audio(AUDIO_FILE)
            if not recorded:
                print("No speech detected. Please try again.")
                continue

            # Convert speech to text
            user_text = speech_to_text(AUDIO_FILE)
            if not user_text:
                print("Sorry, I couldn't understand you.")
                continue

            print("\nYou said:")
            print(user_text)

            # chenk exit command
            if user_text.lower().strip() in EXIT_COMMANDS:
                print("\nAI Response:")
                print("Goodbye!")
                text_to_speech("Goodbye!")
                break

            # Generate AI response
            ai_response = generate_response(user_text)
            if not ai_response:
                print("Sorry, i couldn't get a response from the AI.")
                continue

            print("\nAI Response:")
            print(ai_response)

            # Convert AI response to speech
            text_to_speech(ai_response)

            print("\n" + "-" * 50)

        # keyboard interruption

        except KeyboardInterrupt:
            print("\nAssistant stoped.")
            break

        # unexpected error

        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("The assistant will try again.")


if __name__ == "__main__":
    main()