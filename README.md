# 🎙️ AI Voice Assistant

An AI Voice Assistant built with Python and Streamlit.

The assistant allows users to communicate with an AI using their voice. The user's speech is converted into text, sent to an LLM API, and the AI response is converted back into speech.

## 🚀 Features

- 🎤 Voice input through the microphone
- 🗣️ Speech-to-Text
- 🤖 AI-generated responses
- 🔊 Text-to-Speech
- 💬 Conversation history
- 🗑️ Clear Conversation button
- 🌐 Web-based user interface
- 📦 Modular Python project structure

## 🔄 How It Works

The assistant follows this pipeline:

**🎤 Speech → 📝 Text → 🤖 AI → 💬 Response → 🔊 Speech**

1. The user speaks through the microphone.
2. The recorded audio is converted into text.
3. The text is sent to the AI/LLM API.
4. The AI generates a response.
5. The response is converted into speech.
6. The user can hear the AI response.
7. The conversation is displayed in the conversation panel.

## 🛠️ Technologies Used

- Python
- Streamlit
- Streamlit Mic Recorder
- SpeechRecognition
- pyttsx3
- Requests
- LLM API