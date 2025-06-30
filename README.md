# My AI Assistant (我的AI助手)

一个可定制、带语音功能的个性化 AI 助手项目。由 Python 驱动，可以连接到你自己的 AI 服务。

## ✨ 核心功能

- **智能对话**: 基于大型语言模型 (如 Gemini) 提供强大的对话能力。
- **语音输出 (TTS)**: 集成 OpenAI 的文本转语音服务，让 AI 能“说话”。
- **长期记忆**: AI 能够记住之前的对话内容，实现连贯的上下文交流。
- **可定制人设**: 你可以在 `config.py` 文件中为你的 AI 设定独特的名字、性格和说话风格。
- **可配置 API**: 轻松配置使用你自己的 API 中转服务。

## 🛠️ 技术栈

- **后端**: Python 3
- **语言模型**: Google Gemini Pro (通过 API 调用)
- **语音合成**: OpenAI TTS (通过 API 调用)
- **依赖库**: `requests`, `pygame`

## 🚀 安装与运行

**1. 克隆仓库**
```bash
git clone <your-repository-url>
cd my_ai_assistant
```

**2. 安装依赖**
```bash
pip install -r requirements.txt
```

**3. 配置项目**

这是最重要的一步！将模板文件 `config.example.py` 复制一份，并重命名为 `config.py`。

```bash
cp config.example.py config.py
```

然后，打开你新创建的 `config.py` 文件进行修改。

> **⚠️ 重要安全提示:**
> 我们已经将 `config.py` 加入了 `.gitignore`。请**不要**强制将它上传到 GitHub，以保护你的 API 密钥安全。

你需要修改 `config.py` 中的以下变量：

- `API_BASE_URL`: 你的 API 中转服务地址 (例如: `"https://api.agluo.com/v1"`)。
- `API_KEY`: 你的 API 密钥。
- `LLM_MODEL`: 你想使用的语言模型 (例如: `"gemini-2.5-pro"`)。
- `TTS_MODEL`: 你想使用的语音模型 (例如: `"tts-1"`)。
- `AI_PERSONA`: 在这里定义你的 AI 的详细人设。

**4. 运行助手**
```bash
python main.py
```

## 💬 使用示例

```
AI 助手已启动。输入 '退出' 来结束程序。
你: 你好
AI: 正在思考...
AI: 叫本喵有什么事吗，铲屎官喵~
AI: 正在生成语音...
```

---
*这个项目是在 Roo 的帮助下创建的。*