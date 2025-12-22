# api_client.py

import requests
import base64
import os

def encode_image_to_base64(image_path: str) -> str:
    """
    将图片文件编码为 base64 字符串。
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_image_mime_type(image_path: str) -> str:
    """
    根据文件扩展名获取图片的 MIME 类型。
    """
    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp"
    }
    return mime_types.get(ext, "image/jpeg")

def get_llm_response(history: list, api_key: str, base_url: str, model: str, image_path: str | None = None) -> str:
    """
    根据对话历史调用语言模型 API 获取回复。
    支持可选的图片参数，用于多模态对话。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # 如果有图片，需要修改最后一条用户消息为多模态格式
    messages_to_send = []
    for msg in history:
        messages_to_send.append(msg.copy())
    
    # 如果提供了图片路径，将最后一条用户消息转换为多模态格式
    if image_path and os.path.exists(image_path):
        # 找到最后一条用户消息并转换为多模态格式
        for i in range(len(messages_to_send) - 1, -1, -1):
            if messages_to_send[i]["role"] == "user":
                text_content = messages_to_send[i]["content"]
                base64_image = encode_image_to_base64(image_path)
                mime_type = get_image_mime_type(image_path)
                
                messages_to_send[i]["content"] = [
                    {
                        "type": "text",
                        "text": text_content if text_content else "请描述这张图片"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
                break
    
    # 注意：这里的 body 结构需要根据你的 newapi 文档进行调整
    # 这是一个兼容 OpenAI API 格式的示例
    body = {
        "model": model,
        "messages": messages_to_send
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=body
        )
        response.raise_for_status()  # 如果请求失败 (非 2xx 状态码)，则会抛出异常
        
        # 解析响应，获取模型的回复内容
        # 这同样需要根据你的 newapi 的具体返回格式进行调整
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        # 将具体的网络错误或服务器错误重新抛出
        raise ConnectionError(f"调用 LLM API 失败: {e}") from e

def get_tts_audio(text: str, api_key: str, base_url: str, model: str, speed: float) -> bytes:
    """
    调用 TTS API 获取语音数据。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # 注意：这里的 body 结构需要根据你的 newapi 文档进行调整
    body = {
        "model": model,
        "input": text,
        "voice": "nova",  # 这是一个清晰的女性声音
        "speed": speed
    }
    
    try:
        response = requests.post(
            f"{base_url}/audio/speech",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        
        # API 应该直接返回音频数据
        return response.content
        
    except requests.exceptions.RequestException as e:
        # 将具体的网络错误或服务器错误重新抛出
        raise ConnectionError(f"调用 TTS API 失败: {e}") from e

def get_memory_summary(history: list, api_key: str, base_url: str, model: str) -> str:
    """调用 LLM 对话历史进行总结，提取关键信息。"""
    
    summary_prompt = {
        "role": "system",
        "content": """
你是一个顶级的对话摘要分析师。你的任务是从一段对话历史中，像侦探一样找出关于“用户”的、具有**长期价值**的、可作为永久记忆的**核心事实**。

你需要严格遵守以下规则：
1.  **判断长期价值**：在提取任何信息前，先判断“这条信息在一周后、一个月后，是否依然对理解这个用户有帮助？”。只记录那些有长期价值的信息。
2.  **提取核心事实**：只关注关于“用户”的**不变或长期属性**。例如：用户的名字、职业、人生目标、关键的个人经历、坚定的好恶（如“非常喜欢古典音乐”、“对猫毛过敏”）等。
3.  **忽略临时信息**：坚决忽略闲聊、问候、关于天气或当天心情的讨论、一次性的计划（如“我今晚想吃披萨”）以及任何无信息量的对话。
4.  **简洁输出**：以最简洁的第三人称陈述句输出，每条信息点占一行。
5.  **无信息则留空**：如果对话中没有出现任何符合上述标准的关键信息，请务必只返回一个空字符串。
6.  **禁止额外内容**：绝对不要添加任何额外的解释、标题、引言或总结性的话语。

例如，如果输入以下对话：
[
  {"role": "user", "content": "你好"},
  {"role": "assistant", "content": "你好呀！"},
  {"role": "user", "content": "我叫小王，我有一只叫“旺财”的柯基犬。"},
  {"role": "assistant", "content": "柯基很可爱！"},
  {"role": "user", "content": "是啊，不过我不喜欢吃洋葱。"},
]

你应该输出：
用户的名字是小王。
用户有一只叫“旺财”的柯基犬。
用户不喜欢吃洋葱。

再例如，如果输入以下对话：
[
  {"role": "user", "content": "今天天气真好"},
  {"role": "assistant", "content": "是呀，很适合出去玩。"},
  {"role": "user", "content": "我最喜欢的游戏是《赛博朋克2077》。"},
  {"role": "assistant", "content": "哦，那是一款很棒的游戏！"},
  {"role": "user", "content": "你觉得呢？"},
  {"role": "assistant", "content": "我只是一个AI，没有个人喜好哦。"},
]

你应该输出：
用户最喜欢的游戏是《赛博朋克2077》。
"""
    }
    
    request_history = [summary_prompt] + history

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    body = {
        "model": model,
        "messages": request_history
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"调用记忆总结 API 时发生错误: {e}")
        return "" # 出错时返回空字符串