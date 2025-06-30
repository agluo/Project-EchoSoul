# api_client.py

import requests
import config

def get_llm_response(history: list) -> str:
    """
    根据对话历史调用语言模型 API 获取回复。
    """
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json",
    }
    
    # 注意：这里的 body 结构需要根据你的 newapi 文档进行调整
    # 这是一个兼容 OpenAI API 格式的示例
    body = {
        "model": config.LLM_MODEL,
        "messages": history
    }
    
    try:
        response = requests.post(
            f"{config.API_BASE_URL}/chat/completions",
            headers=headers,
            json=body
        )
        response.raise_for_status()  # 如果请求失败 (非 2xx 状态码)，则会抛出异常
        
        # 解析响应，获取模型的回复内容
        # 这同样需要根据你的 newapi 的具体返回格式进行调整
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.JSONDecodeError:
        print("无法解析服务器返回的 JSON 数据。")
        print(f"状态码: {response.status_code}")
        print(f"返回内容: {response.text}")
        return "抱歉，服务器返回格式错误。"
    except requests.exceptions.RequestException as e:
        print(f"调用 LLM API 时发生网络错误: {e}")
        return "抱歉，我暂时无法回答。"

def get_tts_audio(text: str) -> bytes:
    """
    调用 TTS API 获取语音数据。
    """
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json",
    }
    
    # 注意：这里的 body 结构需要根据你的 newapi 文档进行调整
    body = {
        "model": config.TTS_MODEL,
        "input": text,
        "voice": "nova"  # 这是一个清晰的女性声音
    }
    
    try:
        response = requests.post(
            f"{config.API_BASE_URL}/audio/speech",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        
        # API 应该直接返回音频数据
        return response.content
        
    except requests.exceptions.RequestException as e:
        print(f"调用 TTS API 时发生错误: {e}")
        return None