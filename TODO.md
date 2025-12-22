# Project-EchoSoul - TODO List

这是一个待办事项列表，用于记录我们项目的后续开发计划。

---

## ✅ 已完成功能

### 核心功能
- [x] 现代化 GUI 界面（CustomTkinter）
- [x] 气泡式聊天界面
- [x] LLM 对话功能
- [x] TTS 语音合成与播放
- [x] 长短期记忆系统
- [x] 运行时配置（设置窗口）
- [x] 首次运行引导
- [x] 自定义用户昵称

### 界面美化 (2024-12)
- [x] 优雅紫 + 青色 + 粉色现代配色方案
- [x] 顶部标题栏
- [x] 美化聊天气泡（大圆角、区分颜色）
- [x] 美化设置窗口（带图标标签、API Key 隐藏显示）
- [x] 胶囊形按钮和输入框
- [x] 语音播放按钮美化

### 图片功能 (2024-12)
- [x] 发送图片功能（多模态对话）
- [x] 图片选择按钮（📷）
- [x] 图片预览与取消
- [x] **剪贴板粘贴图片**（Ctrl+V 截图直接粘贴）
- [x] **聊天气泡显示图片缩略图**

---

## 🎯 下次首要任务 (发布新版本)

1.  **✅ 最终功能测试**:
    - [ ] 测试图片发送功能（选择文件、截图粘贴、预览、发送）
    - [ ] 测试多模态对话（需要视觉模型如 gpt-4o、gemini-2.0-flash）
    - [ ] 测试界面美化效果

2.  **⬆️ 提交到 GitHub**:
    - [ ] 将所有新功能提交到 GitHub
    ```bash
    git add .
    git commit -m "feat: 图片发送功能 + 界面美化 + 剪贴板粘贴"
    git push
    ```

3.  **📦 打包 `.exe` 文件**:
    - [ ] 使用 PyInstaller 打包
    ```bash
    pyinstaller gui.py --onefile --windowed --name="Project-EchoSoul" --add-data="config.example.py;." --version-file version.txt
    ```

4.  **🎉 创建 GitHub Release**:
    - [ ] 创建新版本（如 `v1.1.0`）
    - [ ] 上传 `Project-EchoSoul.exe`

---

## 🚀 未来的梦想清单 (可选功能)

- [ ] **连接虚拟形象**: 连接 VTube Studio，让"Miko"拥有能动的形象
- [ ] **支持语音输入 (ASR)**: 实现语音对话闭环
- [ ] **更多 UI 与体验优化**:
    - [ ] 界面图标
    - [ ] "清空聊天记录"按钮
    - [ ] "清除长期记忆"按钮
    - [ ] 主题切换（浅色/深色）
    - [ ] 聊天历史导出
- [ ] **图片功能增强**:
    - [ ] 支持拖拽图片到窗口
    - [ ] 点击缩略图查看大图

---

## 📁 项目结构

```
Project-EchoSoul/
├── gui.py              # 主程序 - GUI 界面
├── api_client.py       # API 客户端 - LLM/TTS 调用
├── config.py           # 配置文件（运行时生成）
├── memory.txt          # 长期记忆存储
├── requirements.txt    # Python 依赖
├── README.md           # 英文说明
├── README.zh-CN.md     # 中文说明
├── TODO.md             # 待办事项
└── version.txt         # 版本信息
```

## 🎨 当前主题配色

| 颜色 | 用途 | 色值 |
|------|------|------|
| 🟣 优雅紫 | 主色调、用户气泡 | `#6C5CE7` |
| 🔵 青色 | AI气泡、次要色 | `#00CEC9` |
| 🩷 粉色 | 强调色 | `#FD79A8` |
| ⬛ 深蓝 | 背景 | `#1A1A2E` |
