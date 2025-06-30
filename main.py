# main.py

import api_client
import pygame
import io
import config

def initialize_pygame():
    """初始化 Pygame Mixer."""
    pygame.mixer.init()

def play_audio(audio_data: bytes):
    """使用 Pygame 播放音频数据."""
    if not audio_data:
        print("没有接收到有效的音频数据。")
        return
        
    try:
        # 将 bytes 数据加载到内存中的文件
        audio_file = io.BytesIO(audio_data)
        
        # 从内存文件加载音频并播放
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"播放音频时发生错误: {e}")

def main():
    """主函数."""
    initialize_pygame()
    
    # 定义系统提示词和对话历史
    system_prompt = {
        "role": "system",
        "content": config.AI_PERSONA
    }
    conversation_history = [system_prompt]
    
    print("AI 助手已启动。输入 '退出' 来结束程序。")
    
    while True:
        try:
            prompt = input("你: ")
            if prompt.lower() in ["退出", "exit", "quit"]:
                print("AI 助手已关闭。")
                break

            # 将用户输入添加到历史记录
            conversation_history.append({"role": "user", "content": prompt})
            
            # 1. 获取 LLM 回复
            print("AI: 正在思考...")
            ai_response = api_client.get_llm_response(conversation_history)
            print(f"AI: {ai_response}")

            # 将 AI 回复也添加到历史记录
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # 2. 获取 TTS 音频
            print("AI: 正在生成语音...")
            audio_data = api_client.get_tts_audio(ai_response)
            
            # 3. 播放音频
            if audio_data:
                play_audio(audio_data)
            else:
                print("(语音合成失败，请检查 newapi 配置或密钥权限)")

        except KeyboardInterrupt:
            print("\nAI 助手已关闭。")
            break
        except Exception as e:
            print(f"程序发生未知错误: {e}")

if __name__ == "__main__":
    main()