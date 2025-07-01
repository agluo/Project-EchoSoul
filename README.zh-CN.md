# Project-EchoSoul (回声灵魂计划)

一个可定制、带语音功能的个性化 AI 助手项目。由 Python 驱动，可以连接到你自己的 AI 服务。

## ✨ 核心功能

- **现代图形界面 (GUI)**: 一个基于 CustomTkinter 构建的、时尚的聊天气泡风格图形界面。
- **智能对话**: 基于大型语言模型 (如 Gemini) 提供强大的对话能力。
- **语音输出 (TTS)**: 集成 OpenAI 的文本转语音服务，让 AI 能“说话”。
- **高级记忆系统**: 独具特色的两层记忆系统。AI 会将关于用户的关键事实智能地总结并存入长期记忆，从而实现真正个性化、有上下文的互动。
- **运行时配置**: 用户友好的设置窗口允许你随时动态修改 API 密钥、模型、AI 人设等信息。
- **首次运行向导**: 首次启动程序时会自动弹出引导设置，无需再手动编辑配置文件。

## 🚀 快速上手 (普通用户)

使用本项目的最简单方式，是直接下载我们为您打包好的 Windows 最新版本。

**[➡️ 前往 Releases 页面下载最新版本！](https://github.com/agluo/Project-EchoSoul/releases/latest)**

您只需下载 `.exe` 文件，将它放在任意文件夹中，然后双击运行即可。本程序是绿色、免安装的。

> **⚠️ 重要前提：API 地址与密钥**
>
> 为了正常运行，本程序需要一个能兼容 OpenAI API 格式、并且能同时调用语言模型（如 Google Gemini）和文本转语音模型（如 OpenAI TTS）的 API 服务地址。
>
> 这通常意味着您需要使用一个**第三方代理或中转服务**，由该服务将请求分别发给对应的上游模型。您在设置中填写的 `API_BASE_URL` 和 `API_KEY` 必须是用于该中转服务的。
>
> **程序会在首次启动时，引导您填入您的服务地址和密钥。** 请注意，配置此类服务可能较为复杂，因此本项目更适合熟悉此类 API 代理服务的用户。
>
> #### 设置项说明
> 设置窗口会要求您填写以下信息：
> -   **`API_BASE_URL`**: 你的 API 代理服务的完整 URL 地址。
> -   **`API_KEY`**: 用于访问你的 API 代理服务的密钥。
> -   **`USER_NICKNAME`**: 你希望 AI 如何称呼你。*默认值: `你`*
> -   **`LLM_MODEL`**: 用于对话的语言模型。*默认值: `gemini-2.5-pro`*
> -   **`TTS_MODEL`**: 用于文本转语音的模型。*默认值: `tts-1`*
> -   **`TTS_SPEED`**: 语音的播放速度 (范围 `0.25` 到 `4.0`)。*默认值: `1.0`*
> -   **`AI_PERSONA`**: 关于 AI 性格的详细描述。
> -   **`MEMORY_TRIGGER_THRESHOLD`**: 对话多少轮后触发记忆总结。*默认值: `20`*

---

## 👨‍💻 面向开发者 (从源码构建)

如果您希望修改代码，或自行构建本项目，请遵循以下步骤。

### 1. 技术栈
- **后端**: Python 3
- **语言模型**: Google Gemini Pro (via API)
- **语音合成**: OpenAI TTS (via API)
- **依赖库**: `requests`, `pygame`, `customtkinter`

### 2. 环境设置
**a. 克隆仓库**
```bash
git clone https://github.com/agluo/Project-EchoSoul.git
cd Project-EchoSoul
```

**b. 安装依赖**
```bash
pip install -r requirements.txt
```

### 3. 从源码运行
直接运行 `gui.py` 脚本即可。首次运行时，程序会自动弹出设置窗口。
```bash
python gui.py
```

### 4. 打包发布
本项目已配置好，可使用 PyInstaller 轻松打包成一个独立的 `.exe` 可执行文件。
```bash
pyinstaller gui.py --onefile --windowed --name="Project-EchoSoul" --version-file version.txt
```
最终生成的 `.exe` 文件会位于 `dist` 文件夹内。

---
*这个项目是在 Roo 的帮助下创建的。*