import customtkinter as ctk
import api_client
import pygame
import io
import threading
import os
import importlib
import sys
import tempfile
from tkinter import filedialog
from PIL import Image, ImageGrab

# --- 主题配色 ---
THEME = {
    "primary": "#6C5CE7",        # 主色调 - 优雅紫
    "primary_hover": "#5B4ED6",  # 主色调悬停
    "secondary": "#00CEC9",      # 次要色 - 青色
    "accent": "#FD79A8",         # 强调色 - 粉色
    "user_bubble": "#6C5CE7",    # 用户消息气泡
    "ai_bubble": "#00CEC9",      # AI消息气泡
    "system_bubble": "#636E72",  # 系统消息气泡
    "bg_dark": "#1A1A2E",        # 深色背景
    "bg_medium": "#16213E",      # 中等背景
    "bg_light": "#0F3460",       # 浅色背景
    "text_primary": "#FFFFFF",   # 主要文字
    "text_secondary": "#B2BEC3", # 次要文字
    "border": "#2D3436",         # 边框色
}

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
    """美化的聊天气泡组件"""
    def __init__(self, master, user, message, user_nickname, audio_data=None, replay_callback=None, image_path=None):
        super().__init__(master, fg_color="transparent")
        is_user = user == user_nickname
        is_system = user == "系统"
        anchor = "e" if is_user else "w"
        justify = "right" if is_user else "left"
        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        if is_user:
            content_frame.pack(anchor="e", padx=(80, 0))
        else:
            content_frame.pack(anchor="w", padx=(0, 80))
        
        # 用户名标签 - 更精致的样式
        user_label = ctk.CTkLabel(
            content_frame, 
            text=user, 
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=12, weight="bold"),
            text_color=THEME["text_secondary"]
        )
        user_label.pack(anchor=anchor, padx=12, pady=(0, 2))
        
        # 根据发送者选择气泡颜色
        if is_system:
            bubble_color = THEME["system_bubble"]
        elif is_user:
            bubble_color = THEME["user_bubble"]
        else:
            bubble_color = THEME["ai_bubble"]
        
        # 如果有图片，先显示图片缩略图
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                # 限制缩略图大小
                max_size = (200, 200)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                
                # 图片容器（带圆角背景）
                image_container = ctk.CTkFrame(
                    content_frame,
                    fg_color=bubble_color,
                    corner_radius=16
                )
                image_container.pack(anchor=anchor, padx=12, pady=(0, 4))
                
                image_label = ctk.CTkLabel(
                    image_container,
                    image=ctk_image,
                    text=""
                )
                image_label.image = ctk_image  # 保持引用
                image_label.pack(padx=8, pady=8)
            except Exception as e:
                print(f"加载图片缩略图失败: {e}")
        
        # 消息气泡 - 更大的圆角和更好的内边距（如果有文字消息才显示）
        if message:
            self.message_label = ctk.CTkLabel(
                content_frame, 
                text=message, 
                wraplength=420, 
                justify=justify,
                fg_color=bubble_color, 
                text_color=THEME["text_primary"], 
                corner_radius=16,
                font=ctk.CTkFont(family="Microsoft YaHei UI", size=14)
            )
            self.message_label.pack(anchor=anchor, padx=12, pady=(0, 4), ipady=10, ipadx=14)
        else:
            self.message_label = None
        
        # AI消息的播放按钮 - 更美观的样式
        if not is_user and not is_system and replay_callback:
            self.replay_button = ctk.CTkButton(
                content_frame, 
                text="🔊 播放语音", 
                width=90,
                height=28,
                corner_radius=14,
                fg_color=THEME["bg_light"],
                hover_color=THEME["primary"],
                font=ctk.CTkFont(size=12),
                command=lambda: replay_callback(audio_data)
            )
            self.replay_button.pack(anchor=anchor, padx=12, pady=(0, 8))
            if not audio_data:
                self.replay_button.configure(state="disabled", fg_color=THEME["border"])
                
    def update_with_final_data(self, new_text, audio_data, replay_callback):
        self.message_label.configure(text=new_text)
        if hasattr(self, 'replay_button') and self.replay_button:
            if audio_data:
                self.replay_button.configure(
                    state="normal", 
                    fg_color=THEME["bg_light"],
                    command=lambda: replay_callback(audio_data)
                )
            else:
                self.replay_button.configure(state="disabled", fg_color=THEME["border"])

class SettingsWindow(ctk.CTkToplevel):
    """美化的设置窗口"""
    def __init__(self, master):
        super().__init__(master)
        self.title("⚙️ 设置")
        self.geometry("500x650")
        self.transient(master)
        self.grab_set()
        self.app = master
        self.configure(fg_color=THEME["bg_dark"])
        
        # 标题
        title_label = ctk.CTkLabel(
            self, 
            text="✨ EchoSoul 设置",
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=24, weight="bold"),
            text_color=THEME["primary"]
        )
        title_label.pack(pady=(20, 10))
        
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color=THEME["bg_medium"],
            corner_radius=16
        )
        self.scrollable_frame.pack(padx=20, pady=10, expand=True, fill="both")
        
        # 通用标签样式
        label_font = ctk.CTkFont(family="Microsoft YaHei UI", size=13, weight="bold")
        entry_font = ctk.CTkFont(family="Microsoft YaHei UI", size=13)
        
        # 昵称设置
        self.nickname_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="👤 你的昵称",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.nickname_label.pack(pady=(15, 5), padx=15, anchor="w")
        self.nickname_entry = ctk.CTkEntry(
            self.scrollable_frame,
            font=entry_font,
            height=38,
            corner_radius=10,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"]
        )
        self.nickname_entry.pack(pady=5, padx=15, fill="x")
        self.nickname_entry.insert(0, self.app.user_nickname)

        # API Key
        self.api_key_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="🔑 API Key",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.api_key_label.pack(pady=(15, 5), padx=15, anchor="w")
        self.api_key_entry = ctk.CTkEntry(
            self.scrollable_frame,
            font=entry_font,
            height=38,
            corner_radius=10,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"],
            show="•"
        )
        self.api_key_entry.pack(pady=5, padx=15, fill="x")
        self.api_key_entry.insert(0, self.app.api_key)
        
        # Base URL
        self.base_url_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="🌐 API Base URL",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.base_url_label.pack(pady=(15, 5), padx=15, anchor="w")
        self.base_url_entry = ctk.CTkEntry(
            self.scrollable_frame,
            font=entry_font,
            height=38,
            corner_radius=10,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"]
        )
        self.base_url_entry.pack(pady=5, padx=15, fill="x")
        self.base_url_entry.insert(0, self.app.base_url)
        
        # LLM Model
        self.llm_model_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="🤖 LLM Model",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.llm_model_label.pack(pady=(15, 5), padx=15, anchor="w")
        self.llm_model_entry = ctk.CTkEntry(
            self.scrollable_frame,
            font=entry_font,
            height=38,
            corner_radius=10,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"]
        )
        self.llm_model_entry.pack(pady=5, padx=15, fill="x")
        self.llm_model_entry.insert(0, self.app.llm_model)
        
        # TTS Model
        self.tts_model_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="🔊 TTS Model",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.tts_model_label.pack(pady=(15, 5), padx=15, anchor="w")
        self.tts_model_entry = ctk.CTkEntry(
            self.scrollable_frame,
            font=entry_font,
            height=38,
            corner_radius=10,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"]
        )
        self.tts_model_entry.pack(pady=5, padx=15, fill="x")
        self.tts_model_entry.insert(0, self.app.tts_model)
        
        # 语速滑块
        self.speed_label_value = ctk.CTkLabel(
            self.scrollable_frame, 
            text=f"⚡ 语速: {self.app.tts_speed:.2f}x",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.speed_label_value.pack(pady=(15, 5), padx=15, anchor="w")
        self.speed_slider = ctk.CTkSlider(
            self.scrollable_frame, 
            from_=0.25, 
            to=4.0, 
            command=self.update_speed_label,
            progress_color=THEME["primary"],
            button_color=THEME["secondary"],
            button_hover_color=THEME["accent"]
        )
        self.speed_slider.pack(pady=5, padx=15, fill="x")
        self.speed_slider.set(self.app.tts_speed)
        
        # AI Persona
        self.persona_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="🎭 AI Persona",
            font=label_font,
            text_color=THEME["text_primary"]
        )
        self.persona_label.pack(pady=(15, 5), padx=15, anchor="w")
        self.persona_textbox = ctk.CTkTextbox(
            self.scrollable_frame, 
            height=150,
            corner_radius=10,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"],
            font=entry_font
        )
        self.persona_textbox.pack(pady=5, padx=15, expand=True, fill="both")
        self.persona_textbox.insert("1.0", self.app.ai_persona)
        
        # 保存按钮
        self.save_button = ctk.CTkButton(
            self, 
            text="💾 保存设置", 
            command=self.save_and_close,
            height=45,
            corner_radius=22,
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=15, weight="bold"),
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"]
        )
        self.save_button.pack(pady=20, padx=20, fill="x")
        
    def update_speed_label(self, value):
        self.speed_label_value.configure(text=f"⚡ 语速: {value:.2f}x")
        
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
        self.title("✨ Project EchoSoul - AI 伴侣")
        self.geometry("800x700")
        self.configure(fg_color=THEME["bg_dark"])
        
        # --- Load Config ---
        self.load_config()

        # --- 顶部标题栏 ---
        self.header_frame = ctk.CTkFrame(self, fg_color=THEME["bg_medium"], corner_radius=0, height=60)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🌟 EchoSoul",
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=22, weight="bold"),
            text_color=THEME["primary"]
        )
        self.title_label.pack(side="left", padx=20, pady=15)
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="与 Miko 聊天中...",
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
            text_color=THEME["text_secondary"]
        )
        self.subtitle_label.pack(side="left", padx=5, pady=15)

        # --- 聊天区域 ---
        self.chat_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color=THEME["bg_dark"],
            corner_radius=0
        )
        self.chat_frame.pack(pady=0, padx=0, expand=True, fill="both")
        
        # --- 图片预览框架 ---
        self.image_preview_frame = ctk.CTkFrame(
            self, 
            fg_color=THEME["bg_medium"],
            corner_radius=12
        )
        self.image_preview_frame.pack(pady=(0, 5), padx=15, fill="x")
        self.image_preview_frame.pack_forget()  # 初始隐藏
        
        # --- 底部输入区域 ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color=THEME["bg_medium"], corner_radius=0, height=70)
        self.bottom_frame.pack(pady=0, padx=0, fill="x")
        self.bottom_frame.pack_propagate(False)
        
        # 内部容器，用于居中和边距
        self.input_container = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.input_container.pack(fill="both", expand=True, padx=15, pady=12)
        
        # 图片选择按钮
        self.image_button = ctk.CTkButton(
            self.input_container, 
            text="📷", 
            width=45,
            height=45,
            corner_radius=22,
            fg_color=THEME["bg_light"],
            hover_color=THEME["primary"],
            font=ctk.CTkFont(size=18),
            command=self.select_image
        )
        self.image_button.pack(side="left", padx=(0, 10))
        
        # 输入框
        self.entry_box = ctk.CTkEntry(
            self.input_container, 
            placeholder_text="和 Miko 说点什么吧...", 
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=14),
            height=45,
            corner_radius=22,
            border_color=THEME["border"],
            fg_color=THEME["bg_light"]
        )
        self.entry_box.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.entry_box.bind("<Return>", self.send_message)
        
        # 发送按钮
        self.send_button = ctk.CTkButton(
            self.input_container, 
            text="发送 ➤", 
            width=90,
            height=45,
            corner_radius=22,
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=14, weight="bold"),
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            command=self.send_message
        )
        self.send_button.pack(side="left", padx=(0, 10))
        
        # 设置按钮
        self.settings_button = ctk.CTkButton(
            self.input_container, 
            text="⚙️", 
            width=45,
            height=45,
            corner_radius=22,
            fg_color=THEME["bg_light"],
            hover_color=THEME["secondary"],
            font=ctk.CTkFont(size=18),
            command=self.open_settings_window
        )
        self.settings_button.pack(side="left")

        # --- Initialize Backend ---
        pygame.mixer.init()
        self.conversation_history = []
        self.settings_window = None
        self.is_speaking = False
        self.thinking_bubble = None
        self.is_summarizing = False # 为记忆总结添加状态锁
        self.long_term_memory = ""
        self.pending_image_path = None  # 待发送的图片路径
        self.temp_image_dir = tempfile.mkdtemp(prefix="echosoul_")  # 临时图片目录
        
        # 绑定粘贴快捷键
        self.bind("<Control-v>", self.paste_from_clipboard)
        self.entry_box.bind("<Control-v>", self.paste_from_clipboard)
        self.image_preview_label = None  # 图片预览标签
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

    def paste_from_clipboard(self, event=None):
        """从剪贴板粘贴图片"""
        try:
            # 尝试从剪贴板获取图片
            clipboard_image = ImageGrab.grabclipboard()
            
            if clipboard_image is not None and isinstance(clipboard_image, Image.Image):
                # 生成临时文件路径
                import time
                temp_filename = f"clipboard_{int(time.time() * 1000)}.png"
                temp_path = os.path.join(self.temp_image_dir, temp_filename)
                
                # 保存图片到临时文件
                clipboard_image.save(temp_path, "PNG")
                
                # 显示预览
                self.pending_image_path = temp_path
                self.show_image_preview(temp_path)
                
                return "break"  # 阻止默认的粘贴行为
            
            # 如果不是图片，检查是否是文件路径列表（从文件管理器复制的图片文件）
            elif clipboard_image is not None and isinstance(clipboard_image, list):
                for file_path in clipboard_image:
                    if isinstance(file_path, str) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
                        self.pending_image_path = file_path
                        self.show_image_preview(file_path)
                        return "break"
            
            # 不是图片，允许正常的文本粘贴
            return None
            
        except Exception as e:
            # 发生错误时允许正常粘贴
            print(f"剪贴板图片获取失败: {e}")
            return None

    def select_image(self):
        """打开文件对话框选择图片"""
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.gif *.webp *.bmp"),
            ("所有文件", "*.*")
        ]
        image_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=filetypes
        )
        if image_path:
            self.pending_image_path = image_path
            self.show_image_preview(image_path)
    
    def show_image_preview(self, image_path: str):
        """显示图片预览"""
        try:
            # 清除之前的预览
            self.clear_image_preview()
            
            # 加载并缩放图片
            img = Image.open(image_path)
            img.thumbnail((120, 120))  # 限制预览大小
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            # 预览容器
            preview_container = ctk.CTkFrame(
                self.image_preview_frame,
                fg_color=THEME["bg_light"],
                corner_radius=10
            )
            preview_container.pack(side="left", padx=10, pady=8)
            
            # 创建预览框架内容
            self.image_preview_label = ctk.CTkLabel(
                preview_container, 
                image=ctk_image, 
                text=""
            )
            self.image_preview_label.image = ctk_image  # 保持引用
            self.image_preview_label.pack(padx=8, pady=8)
            
            # 取消按钮
            self.cancel_image_button = ctk.CTkButton(
                self.image_preview_frame, 
                text="✕ 取消", 
                width=70, 
                height=32,
                corner_radius=16,
                fg_color=THEME["accent"],
                hover_color="#E84393",
                font=ctk.CTkFont(size=12),
                command=self.clear_image_preview
            )
            self.cancel_image_button.pack(side="left", padx=10, pady=8)
            
            # 提示文字
            hint_label = ctk.CTkLabel(
                self.image_preview_frame,
                text="图片已选择，可输入描述后发送",
                font=ctk.CTkFont(size=12),
                text_color=THEME["text_secondary"]
            )
            hint_label.pack(side="left", padx=10)
            
            # 显示预览框架
            self.image_preview_frame.pack(pady=(0, 5), padx=15, fill="x", before=self.bottom_frame)
            self.pending_image_path = image_path
            
        except Exception as e:
            self.add_chat_bubble("系统", f"无法加载图片预览: {e}")
            self.pending_image_path = None
    
    def clear_image_preview(self):
        """清除图片预览"""
        self.pending_image_path = None
        for widget in self.image_preview_frame.winfo_children():
            widget.destroy()
        self.image_preview_frame.pack_forget()

    def send_message(self, event=None):
        prompt = self.entry_box.get()
        # 允许只发送图片（无文字）或只发送文字
        if (not prompt and not self.pending_image_path) or self.is_speaking:
            return
        pygame.mixer.music.stop()
        
        # 获取当前图片路径
        image_path = self.pending_image_path
        
        # 发送带图片的聊天气泡
        self.add_chat_bubble(self.user_nickname, prompt, image_path=image_path)
        self.entry_box.delete(0, "end")
        
        # 清除预览
        self.clear_image_preview()
        
        thread = threading.Thread(target=self.get_ai_response, args=(prompt, image_path))
        thread.start()

    def get_ai_response(self, prompt, image_path=None):
        self.thinking_bubble = None
        try:
            self.is_speaking = True
            self.after(0, self.send_button.configure, {"state": "disabled"})

            # 存储用户消息（纯文本形式，图片不存入历史）
            user_content = prompt if prompt else "[用户发送了一张图片]"
            self.conversation_history.append({"role": "user", "content": user_content})
            
            # 分别构建人设和长期记忆的系统指令
            # 动态构建系统指令，告知 AI 当前用户的昵称
            persona_prompt = self.ai_persona + f'\n\n--- 对话者信息 ---\n当前用户的昵称是"{self.user_nickname}"。请在对话中优先使用这个昵称来称呼用户，而不是"铲屎官"。'
            
            request_history = [
                {"role": "system", "content": persona_prompt},
                {"role": "system", "content": f"--- 关于用户的长期记忆 (请在对话中参考) ---\n{self.long_term_memory}"}
            ] + self.conversation_history[-self.memory_threshold:]

            self.thinking_bubble = self.add_chat_bubble("Miko", "正在思考喵...")
            
            ai_response = api_client.get_llm_response(request_history, self.api_key, self.base_url, self.llm_model, image_path)
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


    def add_chat_bubble(self, user, message, audio_data=None, image_path=None):
        bubble = ChatBubble(self.chat_frame, user, message, self.user_nickname, audio_data, self.play_audio, image_path)
        anchor = "e" if user == self.user_nickname else "w"
        bubble.pack(fill="x", padx=10, pady=8, anchor=anchor)
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
    ctk.set_default_color_theme("blue")
    app = ChatApp()
    app.mainloop()