[Read in Chinese / 阅读中文版](README.zh-CN.md)

# Project-EchoSoul

A customizable, voice-enabled AI assistant with a unique persona. Powered by Python and ready to connect to your own AI services.

## ✨ Core Features

- **Intelligent Conversation**: Leverages Large Language Models (like Gemini) for powerful conversational abilities.
- **Voice Output (TTS)**: Integrates with OpenAI's Text-to-Speech service to give the AI a voice.
- **Long-term Memory**: The AI remembers previous conversations for coherent, context-aware interactions.
- **Customizable Persona**: Define a unique name, personality, and speaking style for your AI in the `config.py` file.
- **Configurable API**: Easily configure the assistant to use your own API endpoint.

## 🛠️ Tech Stack

- **Backend**: Python 3
- **LLM**: Google Gemini Pro (via API)
- **TTS**: OpenAI TTS (via API)
- **Libraries**: `requests`, `pygame`

## 🚀 Installation and Setup

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd Project-EchoSoul
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure the project**

This is the most important step! Copy the template file `config.example.py` and rename it to `config.py`.

```bash
cp config.example.py config.py
```

Then, open the newly created `config.py` file and fill in your details.

> **⚠️ Important Security Notice:**
> The `config.py` file is already listed in `.gitignore`. **Do not** force push it to GitHub, to keep your API keys safe.

You need to modify the following variables in `config.py`:

- `API_BASE_URL`: Your API endpoint (e.g., `"https://your.proxy.url/v1"`).
- `API_KEY`: Your API key.
- `LLM_MODEL`: The language model you want to use (e.g., `"gemini-2.5-pro"`).
- `TTS_MODEL`: The text-to-speech model you want to use (e.g., `"tts-1"`).
- `AI_PERSONA`: Define the detailed persona of your AI here.

**4. Run the assistant**
```bash
python main.py
```

## 💬 Usage Example

```
AI Assistant is running. Type 'exit' to close.
You: Hello
AI: Thinking...
AI: What do you want, my dear master? Meow~
AI: Generating voice...
```

---
*This project was created with the help of Roo.*