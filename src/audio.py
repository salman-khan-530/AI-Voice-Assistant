import sounddevice as sd
import numpy as np
import wave
import time
from collections import deque

# settings

SAMPLE_RATE = 16000
CHANNELS = 1

CHUNK_DURATION = 0.1

CALIBRATION_DURATION = 1.5

SILENCE_DURATION = 1.5

MAX_RECORDING_DURATION = 60

PRE_BUFFER_DURATION = 0.5

THRESHOLD_MULTIPLIER = 2.5

MICROPHONE_DEVICE = 1

# RMS calculation

def calculate_rms(audio):
    audio = audio.astype(np.float32)
    return np.sqrt(np.mean(audio ** 2))


# record audio

def record_audio(file_name="audio.wav"):
    chunk_size = int(
        SAMPLE_RATE * CHUNK_DURATION
    )

    print("\nPreparing microphone...")
    print("Please remain quiet for calibration...")

    calibration_chunks = []


    with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            device=MICROPHONE_DEVICE,
            blocksize=chunk_size
    ) as stream:
        # claibration
        calibration_start = time.time()

        while time.time() - calibration_start < CALIBRATION_DURATION:

            chunk, overflowed = stream.read(chunk_size)

            calibration_chunks.append(
                chunk.copy()
            )

        noise_levels = [
            calculate_rms(chunk)
            for chunk in calibration_chunks
        ]

        background_noise = np.median(
            noise_levels
        )

        speech_threshold = max(
            background_noise * THRESHOLD_MULTIPLIER,
            20
        )

        print(
            f"Background noise level: "
            f"{background_noise:.2f}"
        )

        print(
            f"Speech threshold: "
            f"{speech_threshold:.2f}"
        )

        print("\nListening...")
        print("Start speaking...")


        # Recording variables


        audio_data = []
        
        pre_buffer = deque(
            maxlen=int(
                PRE_BUFFER_DURATION /
                CHUNK_DURATION
            )
        )
        
        speech_started = False
        silence_start = None
        recording_start = time.time()


        # main recording loop

        while True:

            chunk, overflowed = stream.read(
                chunk_size
            )

            chunk = chunk.copy()

            rms = calculate_rms(chunk)

            # Speech detected

            if rms > speech_threshold:

                if not speech_started:
                    speech_started = True

                    print("Recording started...")

                    # Add audio before speech
                    audio_data.extend(
                        list(pre_buffer)
                    )

                audio_data.append(chunk)

                # User is speaking
                silence_start = None


            # Silence after speech
            
            elif speech_started:
                audio_data.append(chunk)

                if silence_start is None:
                    silence_start = time.time()

                elif (
                    time.time() - silence_start
                    >= SILENCE_DURATION
                ):
                    print("Recording stopped.")

                    break

            # Waiting for speech

            else:

                pre_buffer.append(chunk)


            # Safety timeout

            if (
                time.time() - recording_start
                >= MAX_RECORDING_DURATION
            ):
                print("Maximum recording duration reached.")
                break

    # No speech

    if not speech_started:

        print("No speech detected.")

        return False


    # Combine audio

    audio = np.concatenate(
        audio_data,
        axis=0
    )


    # Save WAV

    with wave.open(file_name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    print(f"Recording saved to {file_name}")

    return True



# test

if __name__ == "__main__":
    record_audio("audio.wav")