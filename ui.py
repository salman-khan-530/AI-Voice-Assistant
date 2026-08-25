import streamlit as st
import html

from streamlit_mic_recorder import mic_recorder
from src.stt import speech_to_text
from src.llm import generate_response
from src.tts import text_to_speech

# Page Configuration

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="wide"
)


# custom css

st.markdown(
    """
    <style>

    /* Conversation box */
    .conversation-box {
    height: 400px;
    overflow-y: auto;
    border: 1px solid #444;
    border-radius: 10px;
    padding: 15px;
    margin-top: 10px;
}

    /* Individual message */
    .message {
        margin-bottom: 25px;
    }

    /* User message heading */
    .user-message {
        font-weight: bold;
        margin-bottom: 5px;
    }

    /* AI message heading */
    .ai-message {
        font-weight: bold;
        margin-bottom: 5px;
    }

    /* Message content */
    .message-content {
        line-height: 1.6;
        word-wrap: break-word;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# station state

if "conversation" not in st.session_state:
    st.session_state.conversation = []



# main heading

st.title("🎙️ AI Voice Assistant")

st.write("Welcome to the AI Voice Assistant. ")

st.divider()


# main page columns

left_column, right_column = st.columns([1.1, 1])


# left side

with left_column:

    st.subheader("🎤 Voice Assistant")


    # clear conversation

    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()

    st.write("")



    # microphone

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        key="voice_recorder"
    )


    # process audio

    if audio:

        st.success("Audio recorded successfully!")

        # Get audio bytes
        audio_bytes = audio["bytes"]

        # Audio file
        audio_file = "audio.wav"

        # Save audio
        with open(audio_file, "wb") as file:

            file.write(audio_bytes)

        st.write("Audio saved successfully.")


        # speech to text


        with st.spinner("🎤 Converting speech to text..."):
            text = speech_to_text(audio_file)


        # check transcription

        if text:
            # Add user's message
            st.session_state.conversation.append(
                {
                    "role": "user",
                    "content": text
                }
            )
            #grnerate ai response
            with st.spinner("🤖 Thinking..."):

                ai_response = generate_response(text)


            # check ai response

            if ai_response:
                st.session_state.conversation.append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )

                #text to speech

                audio_response = text_to_speech(
                    ai_response,
                    "response.wav"
                )

                # play ai voice

                if audio_response:
                    st.audio(
                        audio_response,
                        format="audio/wav",
                        autoplay=True
                    )

            else:
                st.error(
                    "Sorry, I couldn't get a response from the AI."
                )

        else:
            st.warning(
                "Sorry, I couldn't understand you."
            )


# conversation

with right_column:

    st.subheader("💬 Conversation")

    # Create conversation HTML
    conversation_html = """
    <div class="conversation-box">
    """

    # display conversation

    for message in st.session_state.conversation:
        content = html.escape(
            message["content"]
        )

        # user message

        if message["role"] == "user":

            conversation_html += f"""
            <div class="message">

                <div class="user-message">
                    🧑 You
                </div>

                <div class="message-content">
                    {content}
                </div>

            </div>
            """

        # ai message

        else:

            conversation_html += f"""
            <div class="message">

                <div class="ai-message">
                    🤖 AI Assistant
                </div>

                <div class="message-content">
                    {content}
                </div>

            </div>
            """


    # Close conversation box
    conversation_html += """
    </div>
    """

    # display html

    st.html(conversation_html)