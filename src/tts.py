import pyttsx3



def text_to_speech(text, output_file="response.wav"):
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        engine.stop()
        return output_file

        
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return None

if __name__ == "__main__":

    text = "Hello! I am your AI voice assistant."

    audio_file = text_to_speech(
        text,
        "response.wav"
    )

    print("Audio file:", audio_file)