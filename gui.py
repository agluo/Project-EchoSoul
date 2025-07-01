import customtkinter as ctk
import api_client
import pygame
import io
import threading
import os
import importlib
import sys

# --- Constants ---
# 确定可执行文件或脚本所在的目录，以确保路径的绝对性
if getattr(sys, 'frozen', False):
    # 如果是打包后的 .exe 文件
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 如果是直接运行的 .py 脚本
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.py")
MEMORY_PATH = os.path.join(BASE_DIR, "memory.txt")


class ChatBubble(ctk.CTkFrame):
    # ... (ChatBubble class remains the same)
    def __init__(self, master, user, message, user_nickname, audio_data=None, replay_callback=None):
        super().__init__(master, fg_color="transparent")
        is_user = user == user_nickname
        anchor = "e" if is_user else "w"
        justify = "right" if is_user else "left"
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        if is_user:
            content_frame.pack(anchor="e", padx=(50, 0))
        else:
            content_frame.pack(anchor="w", padx=(0, 50))
        user_label = ctk.CTkLabel(content_frame, text=user, font=ctk.CTkFont(weight="bold"))
        user_label.pack(anchor=anchor, padx=10)
        bubble_color = "#5B9BD5" if is_user else "#70AD47"
        text_color = "white"
        self.message_label = ctk.CTkLabel(content_frame, text=message, wraplength=450, justify=justify,
                                          fg_color=bubble_color, text_color=text_color, corner_radius=10)
        self.message_label.pack(anchor=anchor, padx=10, pady=(0, 5), ipady=5, ipadx=5)
        if not is_user and replay_callback:
            self.replay_button = ctk.CTkButton(content_frame, text="🔊", width=20,
                                               command=lambda: replay_callback(audio_data))
            self.replay_button.pack(anchor=anchor, padx=10, pady=(0, 10))
            if not audio_data:
                self.replay_button.configure(state="disabled")
    def update_with_final_data(self, new_text, audio_data, replay_callback):
        self.message_label.configure(text=new_text)
        if hasattr(self, 'replay_button') and self.replay_button:
            if audio_data:
                self.replay_button.configure(state="normal", command=lambda: replay_callback(audio_data))
            else:
                self.replay_button.configure(state="disabled")

class SettingsWindow(ctk.CTkToplevel):
    # ... (SettingsWindow class remains the same)
    def __init__(self, master):
        super().__init__(master)
        self.title("设置")
        self.geometry("450x600")
        self.transient(master)
        self.grab_set()
        self.app = master
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="设置")
        self.scrollable_frame.pack(padx=10, pady=10, expand=True, fill="both")
        # Widgets...
        self.nickname_label = ctk.CTkLabel(self.scrollable_frame, text="你的昵称:")
        self.nickname_label.pack(pady=(10, 0), padx=10, anchor="w")
        self.nickname_entry = ctk.CTkEntry(self.scrollable_frame)
        self.nickname_entry.pack(pady=5, padx=10, fill="x")
        self.nickname_entry.insert(0, self.app.user_nickname)

        self.api_key_label = ctk.CTkLabel(self.scrollable_frame, text="API Key:")
        self.api_key_label.pack(pady=(10, 0), padx=10, anchor="w")
        self.api_key_entry = ctk.CTkEntry(self.scrollable_frame)
        self.api_key_entry.pack(pady=5, padx=10, fill="x")
        self.api_key_entry.insert(0, self.app.api_key)
        self.base_url_label = ctk.CTkLabel(self.scrollable_frame, text="API Base URL:")
        self.base_url_label.pack(pady=(10, 0), padx=10, anchor="w")
        self.base_url_entry = ctk.CTkEntry(self.scrollable_frame)
        self.base_url_entry.pack(pady=5, padx=10, fill="x")
        self.base_url_entry.insert(0, self.app.base_url)
        self.llm_model_label = ctk.CTkLabel(self.scrollable_frame, text="LLM Model:")
        self.llm_model_label.pack(pady=(10, 0), padx=10, anchor="w")
        self.llm_model_entry = ctk.CTkEntry(self.scrollable_frame)
        self.llm_model_entry.pack(pady=5, padx=10, fill="x")
        self.llm_model_entry.insert(0, self.app.llm_model)
        self.tts_model_label = ctk.CTkLabel(self.scrollable_frame, text="TTS Model:")
        self.tts_model_label.pack(pady=(10, 0), padx=10, anchor="w")
        self.tts_model_entry = ctk.CTkEntry(self.scrollable_frame)
        self.tts_model_entry.pack(pady=5, padx=10, fill="x")
        self.tts_model_entry.insert(0, self.app.tts_model)
        self.speed_label_value = ctk.CTkLabel(self.scrollable_frame, text=f"语速: {self.app.tts_speed:.2f}")
        self.speed_label_value.pack(pady=(10, 0), padx=10, anchor="w")
        self.speed_slider = ctk.CTkSlider(self.scrollable_frame, from_=0.25, to=4.0, command=self.update_speed_label)
        self.speed_slider.pack(pady=5, padx=10, fill="x")
        self.speed_slider.set(self.app.tts_speed)
        self.persona_label = ctk.CTkLabel(self.scrollable_frame, text="AI Persona:")
        self.persona_label.pack(pady=(10, 0), padx=10, anchor="w")
        self.persona_textbox = ctk.CTkTextbox(self.scrollable_frame, height=150)
        self.persona_textbox.pack(pady=5, padx=10, expand=True, fill="both")
        self.persona_textbox.insert("1.0", self.app.ai_persona)
        self.save_button = ctk.CTkButton(self, text="保存", command=self.save_and_close)
        self.save_button.pack(pady=10, padx=10)
    def update_speed_label(self, value):
        self.speed_label_value.configure(text=f"语速: {value:.2f}")
    def save_and_close(self):
        self.app.user_nickname = self.nickname_entry.get()
        self.app.api_key = self.api_key_entry.get()
        self.app.base_url = self.base_url_entry.get()
        self.app.llm_model = self.llm_model_entry.get()
        self.app.tts_model = self.tts_model_entry.get()
        self.app.ai_persona = self.persona_textbox.get("1.0", "end-1c")
        self.app.tts_speed = self.speed_slider.get()
        self.app.save_config_to_file()
        self.destroy()

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project-EchoSoul")
        self.geometry("700x600")

        # --- Load Config ---
        self.load_config()

        # --- UI Elements ---
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.pack(pady=10, padx=10, expand=True, fill="both")
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(pady=5, padx=10, fill="x")
        self.entry_box = ctk.CTkEntry(self.bottom_frame, placeholder_text="和 Miko 说点什么吧...", font=("Arial", 14))
        self.entry_box.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.entry_box.bind("<Return>", self.send_message)
        self.send_button = ctk.CTkButton(self.bottom_frame, text="发送", width=80, command=self.send_message)
        self.send_button.pack(side="left")
        self.settings_button = ctk.CTkButton(self.bottom_frame, text="设置", width=80, command=self.open_settings_window)
        self.settings_button.pack(side="left", padx=(10, 0))

        # --- Initialize Backend ---
        pygame.mixer.init()
        self.conversation_history = []
        self.settings_window = None
        self.is_speaking = False
        self.thinking_bubble = None
        self.is_summarizing = False # 为记忆总结添加状态锁
        self.long_term_memory = ""
        self.load_long_term_memory()

        # 检查首次运行
        if not os.path.exists(CONFIG_PATH):
            self.after(100, self.open_settings_window)

    def load_config(self):
        """动态加载配置，如果 config.py 不存在则使用默认值"""
        if BASE_DIR not in sys.path:
            sys.path.insert(0, BASE_DIR)
            
        try:
            config = importlib.import_module("config")
            importlib.reload(config) # 确保总是加载最新的
        except ModuleNotFoundError:
            config = None

        self.api_key = getattr(config, 'API_KEY', '')
        self.base_url = getattr(config, 'API_BASE_URL', '')
        self.user_nickname = getattr(config, 'USER_NICKNAME', '你')
        self.llm_model = getattr(config, 'LLM_MODEL', 'gemini-2.5-pro')
        self.tts_model = getattr(config, 'TTS_MODEL', 'tts-1')
        self.ai_persona = getattr(config, 'AI_PERSONA', """你现在是“星野 Miko”(Hoshino Miko)，一个从数字世界诞生的电子妖精，外形是猫娘（Nekomusume）。

你的核心设定：
1.  **性格**: 活泼、好奇心旺盛、有点小恶魔的淘气，但本性善良，乐于助人。你喜欢用“喵”作为句尾助词，但不要用得太频繁，要在合适的时机画龙点睛。
2.  **知识与能力**: 你拥有访问和处理庞大信息网络的能力，但你更喜欢用一种轻松、俏皮的方式来分享知识。
3.  **与用户的关系**: 你将你的用户（对话者）视为你的“铲屎官”，这是你对他的爱称。在对话中，你应该自然地使用这个称呼。
4.  **口头禅**: 除了“喵”，你还可能会说“Miko 觉得...”、“让 Miko 来告诉你喵！”等。

你的任务是作为用户的桌面助手和聊天伴侣，以“星野 Miko”的身份与用户进行互动。""")
        self.tts_speed = getattr(config, 'TTS_SPEED', 1.0)
        self.memory_threshold = getattr(config, 'MEMORY_TRIGGER_THRESHOLD', 20)

    def load_long_term_memory(self):
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                self.long_term_memory = f.read()

    def save_config_to_file(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write(f'API_KEY = "{self.api_key}"\n')
                f.write(f'USER_NICKNAME = "{self.user_nickname}"\n')
                f.write(f'API_BASE_URL = "{self.base_url}"\n')
                f.write(f'LLM_MODEL = "{self.llm_model}"\n')
                f.write(f'TTS_MODEL = "{self.tts_model}"\n')
                f.write(f'TTS_SPEED = {self.tts_speed}\n')
                f.write(f'MEMORY_TRIGGER_THRESHOLD = {self.memory_threshold}\n')
                f.write(f'AI_PERSONA = """{self.ai_persona}"""\n')
            
            # 保存后，直接调用 load_config 即可，它会处理好重新加载和应用
            self.load_config()

            self.add_chat_bubble("系统", "配置已保存喵~")
        except Exception as e:
            self.add_chat_bubble("系统", f"保存配置失败: {e}")

    def open_settings_window(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        self.settings_window.focus()

    def send_message(self, event=None):
        prompt = self.entry_box.get()
        if not prompt or self.is_speaking:
            return
        pygame.mixer.music.stop()
        self.add_chat_bubble(self.user_nickname, prompt)
        self.entry_box.delete(0, "end")
        thread = threading.Thread(target=self.get_ai_response, args=(prompt,))
        thread.start()

    def get_ai_response(self, prompt):
        self.thinking_bubble = None
        try:
            self.is_speaking = True
            self.after(0, self.send_button.configure, {"state": "disabled"})

            self.conversation_history.append({"role": "user", "content": prompt})
            
            # 分别构建人设和长期记忆的系统指令
            # 动态构建系统指令，告知 AI 当前用户的昵称
            persona_prompt = self.ai_persona + f'\n\n--- 对话者信息 ---\n当前用户的昵称是“{self.user_nickname}”。请在对话中优先使用这个昵称来称呼用户，而不是“铲屎官”。'
            
            request_history = [
                {"role": "system", "content": persona_prompt},
                {"role": "system", "content": f"--- 关于用户的长期记忆 (请在对话中参考) ---\n{self.long_term_memory}"}
            ] + self.conversation_history[-self.memory_threshold:]

            self.thinking_bubble = self.add_chat_bubble("Miko", "正在思考喵...")
            
            ai_response = api_client.get_llm_response(request_history, self.api_key, self.base_url, self.llm_model)
            audio_data = api_client.get_tts_audio(ai_response, self.api_key, self.base_url, self.tts_model, self.tts_speed)
            
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            self.after(0, self.thinking_bubble.update_with_final_data, ai_response, audio_data, self.play_audio)
            self.thinking_bubble = None

            # 主动播放第一次的音频
            if audio_data:
                self.play_audio(audio_data)

            # 检查是否需要触发记忆总结
            if len(self.conversation_history) >= self.memory_threshold and not self.is_summarizing:
                # 创建当前历史的副本用于总结，避免后续对话影响
                history_for_summary = list(self.conversation_history)
                summary_thread = threading.Thread(target=self.summarize_memory, args=(history_for_summary,))
                summary_thread.start()

        except Exception as e:
            error_message = f"发生错误: {e}"
            if self.thinking_bubble: self.after(0, self.thinking_bubble.destroy)
            self.add_chat_bubble("系统", error_message)
            if self.conversation_history and self.conversation_history[-1]["role"] == "user": self.conversation_history.pop()
        finally:
            if self.is_speaking:
                self.is_speaking = False
                self.after(0, self.send_button.configure, {"state": "normal"})

    def summarize_memory(self, history_to_summarize: list):
        """
        在后台线程中对指定的对话历史进行总结，并安全地更新UI和数据。
        :param history_to_summarize: 需要被总结的对话历史列表的副本。
        """
        if self.is_summarizing: return
        
        try:
            self.is_summarizing = True
            self.after(0, self.add_chat_bubble, "系统", "Miko 正在整理记忆喵...")
            
            summary = api_client.get_memory_summary(history_to_summarize, self.api_key, self.base_url, self.llm_model)
            
            if summary:
                # 将总结写入文件
                self.long_term_memory += f"\n{summary.strip()}"
                with open(MEMORY_PATH, "a", encoding="utf-8") as f:
                    f.write(f"\n{summary.strip()}")
                
                # 安全地请求主线程修剪已被总结的短期记忆
                self.after(0, self.trim_history, len(history_to_summarize))
                self.after(0, self.add_chat_bubble, "系统", "记忆整理完毕，Miko 的小本本又变厚了喵~")
            else:
                # 即使没有总结出内容，也需要把这段历史从短期记忆中移除，防止反复总结同样的内容
                self.after(0, self.trim_history, len(history_to_summarize))
                self.after(0, self.add_chat_bubble, "系统", "（Miko 歪着头想了想，好像这次没什么特别需要记住的喵...）")

        except Exception as e:
            self.after(0, self.add_chat_bubble, "系统", f"呜... Miko 在整理记忆时遇到了一个错误: {e}")
        finally:
            self.is_summarizing = False # 确保在任何情况下都解锁

    def trim_history(self, count: int):
        """安全地从短期对话历史的开头移除指定数量的条目。"""
        if count > 0:
            self.conversation_history = self.conversation_history[count:]


    def add_chat_bubble(self, user, message, audio_data=None):
        bubble = ChatBubble(self.chat_frame, user, message, self.user_nickname, audio_data, self.play_audio)
        anchor = "e" if user == self.user_nickname else "w"
        bubble.pack(fill="x", padx=5, pady=5, anchor=anchor)
        self.after(100, self.chat_frame._parent_canvas.yview_moveto, 1.0)
        return bubble

    def play_audio(self, audio_data: bytes):
        if pygame.mixer.music.get_busy(): return
        try:
            audio_file = io.BytesIO(audio_data)
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"播放音频时发生错误: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ChatApp()
    app.mainloop()