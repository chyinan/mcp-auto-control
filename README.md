<a id="mcp-桌面自动化代理"></a>
# MCP 桌面自动化代理

[English](#mcp-desktop-automation-agent) | [中文](#mcp-桌面自动化代理)

一个基于 MCP (Model Context Protocol) 的桌面自动化工具，允许 AI 助手通过 MCP 协议控制您的桌面，执行鼠标点击、键盘输入、截图等操作。

## 功能特性

- 🖱️ **鼠标控制**：移动鼠标、点击、双击
- ⌨️ **键盘输入**：文本输入、按键操作、组合键支持
- 📸 **屏幕截图**：获取屏幕截图，标注鼠标位置，支持坐标网格
- 📏 **屏幕信息**：获取屏幕分辨率和鼠标位置
- 🖱️ **滚动操作**：支持屏幕滚动

## 系统要求

- Python 3.8+
- Windows 操作系统（当前版本主要针对 Windows 优化）

## 安装

1. 克隆或下载此项目

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
```

3. 激活虚拟环境：
   - Windows (CMD):
     ```bash
     venv\Scripts\activate
     ```
   - Windows (PowerShell):
     ```powershell
     venv\Scripts\Activate.ps1
     ```

4. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 作为 MCP 服务器运行

1. 确保已安装并配置 Claude Desktop 或其他支持 MCP 的客户端

2. 在 Claude Desktop 的配置文件中添加此服务器：

```json
{
  "mcpServers": {
    "desktop-agent": {
      "command": "python",
      "args": ["D:/mcp_auto_control/desktop_agent.py"]
    }
  }
}
```

3. 重启 Claude Desktop，即可在对话中使用桌面自动化功能

### 直接运行

```bash
python desktop_agent.py
```

## 可用工具

### `get_screen_info()`
获取当前屏幕的分辨率和鼠标位置信息。

### `take_screenshot(show_grid: bool = False)`
获取当前屏幕的截图，并在截图上标注鼠标指针的位置。
- `show_grid`: 如果为 `True`，在截图上绘制坐标网格（每100像素一条线）

### `move_mouse(x: int, y: int)`
将鼠标移动到指定的 (x, y) 坐标。

### `click(x: int = None, y: int = None, double_click: bool = False, verify: bool = False)`
在指定坐标点击鼠标左键。
- `x`, `y`: 点击的坐标（如果未提供，则在当前位置点击）
- `double_click`: 是否双击
- `verify`: 如果为 `True`，点击后会返回当前鼠标位置用于验证

### `type_text(text: str, enter: bool = True)`
在当前焦点位置输入文本。
- `text`: 要输入的文本
- `enter`: 输入完成后是否按下回车键

### `scroll(amount: int)`
滚动屏幕。正数向上滚动，负数向下滚动。

### `press_key(key: str)`
按下指定的键盘按键。
- 常用按键：`'win'`, `'enter'`, `'esc'`, `'tab'`, `'space'`, `'ctrl'`, `'alt'`, `'shift'` 等
- 组合键示例：`'ctrl+c'`, `'alt+tab'`, `'win+r'` 等

## 安全提示

⚠️ **重要**：此工具具有完全控制您桌面的能力，请谨慎使用！

- 已启用 `pyautogui.FAILSAFE = True`：当鼠标移动到屏幕角落时，会强行停止脚本
- 建议在测试环境中先验证功能
- 不要在生产环境或包含敏感信息的系统上使用

## 项目结构

```
mcp_auto_control/
├── desktop_agent.py    # 主程序文件
├── requirements.txt    # 项目依赖
├── README.md          # 项目说明文档
└── .gitignore         # Git 忽略文件配置
```

## 依赖库

- `mcp`: MCP 协议支持
- `pyautogui`: 桌面自动化
- `pillow`: 图像处理

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 注意事项

- 当前版本主要针对 Windows 系统优化
- 截图功能中的字体路径已针对 Windows 系统配置
- 如需在其他操作系统上使用，可能需要调整字体路径配置

---

<a id="mcp-desktop-automation-agent"></a>
# MCP Desktop Automation Agent

[English](#mcp-desktop-automation-agent) | [中文](#mcp-桌面自动化代理)

A desktop automation tool based on MCP (Model Context Protocol) that allows AI assistants to control your desktop through the MCP protocol, performing mouse clicks, keyboard input, screenshots, and other operations.

## Features

- 🖱️ **Mouse Control**: Move mouse, click, double-click
- ⌨️ **Keyboard Input**: Text input, key presses, hotkey support
- 📸 **Screenshot**: Capture screen with mouse position annotation and coordinate grid support
- 📏 **Screen Info**: Get screen resolution and mouse position
- 🖱️ **Scroll Operations**: Support screen scrolling

## System Requirements

- Python 3.8+
- Windows operating system (current version is optimized for Windows)

## Installation

1. Clone or download this project

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows (CMD):
     ```bash
     venv\Scripts\activate
     ```
   - Windows (PowerShell):
     ```powershell
     venv\Scripts\Activate.ps1
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running as an MCP Server

1. Make sure Claude Desktop or other MCP-compatible clients are installed and configured

2. Add this server to Claude Desktop's configuration file:

```json
{
  "mcpServers": {
    "desktop-agent": {
      "command": "python",
      "args": ["D:/mcp_auto_control/desktop_agent.py"]
    }
  }
}
```

3. Restart Claude Desktop to use desktop automation features in conversations

### Direct Run

```bash
python desktop_agent.py
```

## Available Tools

### `get_screen_info()`
Get the current screen resolution and mouse position information.

### `take_screenshot(show_grid: bool = False)`
Capture the current screen and annotate the mouse pointer position on the screenshot.
- `show_grid`: If `True`, draw a coordinate grid on the screenshot (one line per 100 pixels)

### `move_mouse(x: int, y: int)`
Move the mouse to the specified (x, y) coordinates.

### `click(x: int = None, y: int = None, double_click: bool = False, verify: bool = False)`
Click the left mouse button at the specified coordinates.
- `x`, `y`: Click coordinates (if not provided, click at current position)
- `double_click`: Whether to double-click
- `verify`: If `True`, returns the current mouse position after clicking for verification

### `type_text(text: str, enter: bool = True)`
Type text at the current focus position.
- `text`: Text to input
- `enter`: Whether to press Enter after input

### `scroll(amount: int)`
Scroll the screen. Positive numbers scroll up, negative numbers scroll down.

### `press_key(key: str)`
Press the specified keyboard key.
- Common keys: `'win'`, `'enter'`, `'esc'`, `'tab'`, `'space'`, `'ctrl'`, `'alt'`, `'shift'`, etc.
- Hotkey examples: `'ctrl+c'`, `'alt+tab'`, `'win+r'`, etc.

## Security Warning

⚠️ **Important**: This tool has full control over your desktop. Use with caution!

- `pyautogui.FAILSAFE = True` is enabled: Moving the mouse to the screen corner will forcefully stop the script
- It is recommended to verify functionality in a test environment first
- Do not use on production systems or systems containing sensitive information

## Project Structure

```
mcp_auto_control/
├── desktop_agent.py    # Main program file
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file configuration
```

## Dependencies

- `mcp`: MCP protocol support
- `pyautogui`: Desktop automation
- `pillow`: Image processing

## License

This project is licensed under the MIT License.

## Contributing

Issues and Pull Requests are welcome!

## Notes

- Current version is primarily optimized for Windows systems
- Font paths in screenshot functionality are configured for Windows systems
- If using on other operating systems, font path configuration may need adjustment
