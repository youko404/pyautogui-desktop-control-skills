---
name: pyautogui-desktop-control
description: 使用 PyAutoGUI 在本机桌面执行 GUI 自动化，包括读取屏幕分辨率、读取当前鼠标位置、移动鼠标、拖拽、点击、按下或抬起鼠标、滚动、键盘按键、热键、截图、等待和输入文本。用于用户明确要求通过 PyAutoGUI 或桌面自动化来操作鼠标键盘、驱动原生应用、填写表单、点击界面元素、截图留存、做简单 RPA 流程时。
---

# PyAutoGUI Desktop Control

## Overview

使用 `scripts/pyautogui_tool.py` 统一执行常见的桌面自动化动作，减少在任务里重复编写 PyAutoGUI 样板代码。
优先把动作拆成可验证的小步骤：先读状态，再移动，再点击或输入，必要时在步骤之间加短暂停顿。

## Workflow

1. 先确认环境是否可用。
   运行 `python scripts/pyautogui_tool.py screen-size` 或 `mouse-position`。
   如果报错，优先检查 Python 环境是否安装 `pyautogui`，以及系统是否已授予辅助功能、输入监控、录屏等权限。

2. 先观测，再执行。
   读取分辨率和当前鼠标位置，避免直接硬编码坐标。
   如果用户只给了大致位置，先移动到附近，再读取位置并微调。

3. 把动作做成显式步骤。
   常见顺序：`move` -> `click` -> `type`。
   对容易误触的操作，优先使用较短 `--duration` 和显式坐标。

4. 对组合键和快捷操作，优先使用 `hotkey`。
   例如复制、粘贴、保存、关闭窗口。

## Commands

脚本路径：`scripts/pyautogui_tool.py`

常用命令：

```bash
python scripts/pyautogui_tool.py screen-size
python scripts/pyautogui_tool.py mouse-position
python scripts/pyautogui_tool.py move --x 600 --y 420 --duration 0.2
python scripts/pyautogui_tool.py drag --x 900 --y 420 --duration 0.3
python scripts/pyautogui_tool.py click --x 600 --y 420 --button left --clicks 1
python scripts/pyautogui_tool.py mouse-down --x 600 --y 420
python scripts/pyautogui_tool.py mouse-up --x 900 --y 420
python scripts/pyautogui_tool.py type --text "hello world" --interval 0.03
python scripts/pyautogui_tool.py press --key enter
python scripts/pyautogui_tool.py hotkey --keys command v
python scripts/pyautogui_tool.py scroll --clicks -500
python scripts/pyautogui_tool.py screenshot --path /tmp/desktop.png
python scripts/pyautogui_tool.py wait --seconds 1.5
```

## Guidance

- 默认假设在真实桌面会话里运行，不适合无头环境。
- 坐标以主屏幕左上角为原点。
- 需要连续动作时，优先用多个命令串联，而不是一次做过多隐式行为。
- 截图命令支持全屏和区域截图；区域截图必须同时提供 `--x --y --width --height`。
- 如果任务依赖界面元素识别，这个 skill 只负责输入和指针控制；元素定位需要结合截图、视觉识别或其他技能。
- PyAutoGUI 默认启用 failsafe。鼠标快速移到屏幕左上角通常可以中断脚本。

## Resources

### scripts/

- `pyautogui_tool.py`: PyAutoGUI CLI 封装，提供屏幕、鼠标、拖拽、截图、等待、键盘和文本输入操作。
