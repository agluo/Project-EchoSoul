[Read in Chinese / 阅读中文版](README.zh-CN.md)

# Project-EchoSoul

A customizable, voice-enabled AI assistant with a unique persona. Powered by Python and ready to connect to your own AI services.

## ✨ Core Features

- **Modern GUI**: A sleek, chat-bubble-style graphical user interface built with CustomTkinter.
- **Intelligent Conversation**: Leverages Large Language Models (like Gemini) for powerful conversational abilities.
- **Voice Output (TTS)**: Integrates with OpenAI's Text-to-Speech service to give the AI a voice.
- **Advanced Memory System**: Features a robust, two-tier memory system. The AI summarizes key facts about the user into a long-term memory file for truly personalized, context-aware interactions.
- **Runtime Configuration**: A user-friendly settings window allows you to configure API keys, models, AI persona, and more on the fly.
- **User-Friendly Setup**: A guided setup process automatically appears on the first run. No more manual config file editing!

## 🚀 Get Started (for Users)

The easiest way to use Project-EchoSoul is to download the latest pre-packaged version for Windows.

**[➡️ Download the latest release from the Releases page!](https://github.com/your-username/your-repository-name/releases/latest)**

Simply download the `.exe` file, place it in a folder of your choice, and double-click to run. The application is portable and self-contained.

> **⚠️ Important Prerequisite: API Endpoint and Key**
>
> To function, this application requires an API endpoint that is compatible with the OpenAI API format and can access both a language model (like Google's Gemini) and a text-to-speech model (like OpenAI's TTS).
>
> This typically means using a **proxy or a third-party service** that routes requests to the appropriate underlying models. The `API_BASE_URL` and `API_KEY` you provide must be for such a service.
>
> **The application will guide you to enter your endpoint URL and key on the first run.** Setting this up can be complex, so this project is best suited for users who are familiar with using such API proxy services.
>
> #### Settings Explanation
> The settings window will ask for the following details:
> -   **`API_BASE_URL`**: The full URL of your API proxy service.
> -   **`API_KEY`**: The secret key for authenticating with your API proxy service.
> -   **`USER_NICKNAME`**: The name you want the AI to call you. *Default: `You`*
> -   **`LLM_MODEL`**: The language model for conversation. *Default: `gemini-2.5-pro`*
> -   **`TTS_MODEL`**: The text-to-speech model for voice. *Default: `tts-1`*
> -   **`TTS_SPEED`**: The speed of the speech (from `0.25` to `4.0`). *Default: `1.0`*
> -   **`AI_PERSONA`**: A detailed description of the AI's personality.
> -   **`MEMORY_TRIGGER_THRESHOLD`**: How many conversation turns before triggering a memory summary. *Default: `20`*

---

## 👨‍💻 For Developers (Building from Source)

If you want to modify the code or build the project yourself, follow these steps.

### 1. Tech Stack
- **Backend**: Python 3
- **LLM**: Google Gemini Pro (via API)
- **TTS**: OpenAI TTS (via API)
- **Libraries**: `requests`, `pygame`, `customtkinter`

### 2. Setup
**a. Clone the repository**
```bash
git clone <your-repository-url>
cd Project-EchoSoul
```

**b. Install dependencies**
```bash
pip install -r requirements.txt
```

### 3. Running from Source
Simply run the `gui.py` script. The first time you run it, a settings window will automatically appear.

```bash
python gui.py
```

### 4. Packaging
This project is configured for easy packaging into a standalone executable using PyInstaller.
```bash
pyinstaller gui.py --onefile --windowed --name="Project-EchoSoul" --version-file version.txt
```
The final `.exe` will be located in the `dist` folder.

---
*This project was created with the help of Roo.*