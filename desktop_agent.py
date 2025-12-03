from mcp.server.fastmcp import FastMCP, Image
import pyautogui
import io
import base64
from PIL import Image as PILImage, ImageDraw

# 初始化 MCP 服务
# dependencies 参数用于让 Claude Desktop 自动安装依赖（如果是通过 pipx 运行）
mcp = FastMCP("DesktopAgent", dependencies=["pyautogui", "pillow"])

# 安全设置：当鼠标移动到屏幕角落时，强行停止脚本（防止 AI 失控）
pyautogui.FAILSAFE = True

@mcp.tool()
def get_screen_info() -> str:
    """
    获取当前屏幕的分辨率和鼠标位置信息。
    返回格式：屏幕分辨率 + 鼠标坐标。
    在进行鼠标操作前，建议先调用此工具获取屏幕信息。
    """
    screen_width, screen_height = pyautogui.size()
    mouse_x, mouse_y = pyautogui.position()
    return f"屏幕分辨率: {screen_width} x {screen_height}\n鼠标位置: ({mouse_x}, {mouse_y})"

@mcp.tool()
def take_screenshot(show_grid: bool = False) -> Image:
    """
    获取当前屏幕的截图，并在截图上标注鼠标指针的位置。
    当需要查看屏幕内容以决定点击哪里时使用此工具。
    注意：截图只包含鼠标位置的视觉标记，不包含文字信息。
    如需获取屏幕分辨率和鼠标坐标，请调用 get_screen_info() 工具。
    
    Args:
        show_grid: 如果为True，在截图上绘制坐标网格（每100像素一条线），帮助计算准确的点击坐标。
    """
    # 截取全屏
    screenshot = pyautogui.screenshot()
    
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    
    # 获取鼠标当前位置
    mouse_x, mouse_y = pyautogui.position()
    
    # 在截图上绘制鼠标指针标记（不绘制文字，避免遮挡）
    draw = ImageDraw.Draw(screenshot)
    
    # 如果启用网格，绘制坐标网格
    if show_grid:
        grid_spacing = 100
        # 绘制垂直网格线
        for x in range(0, screen_width, grid_spacing):
            draw.line([(x, 0), (x, screen_height)], fill='blue', width=1)
            # 在顶部标注坐标
            try:
                from PIL import ImageFont
                import platform
                font = None
                if platform.system() == "Windows":
                    font_paths = [
                        "C:/Windows/Fonts/msyh.ttc",
                        "C:/Windows/Fonts/simsun.ttc",
                        "C:/Windows/Fonts/arial.ttf",
                    ]
                    for path in font_paths:
                        try:
                            font = ImageFont.truetype(path, 12)
                            break
                        except:
                            continue
                if font is None:
                    font = ImageFont.load_default()
                draw.text((x + 2, 2), str(x), fill='blue', font=font)
            except:
                pass
        
        # 绘制水平网格线
        for y in range(0, screen_height, grid_spacing):
            draw.line([(0, y), (screen_width, y)], fill='blue', width=1)
            # 在左侧标注坐标
            try:
                if font:
                    draw.text((2, y + 2), str(y), fill='blue', font=font)
            except:
                pass
    
    # 绘制一个红色圆圈标记鼠标位置
    circle_radius = 10
    draw.ellipse(
        [(mouse_x - circle_radius, mouse_y - circle_radius),
         (mouse_x + circle_radius, mouse_y + circle_radius)],
        outline='red',
        width=3
    )
    
    # 绘制十字线，更精确地标记鼠标位置
    line_length = 15
    # 水平线
    draw.line(
        [(mouse_x - line_length, mouse_y),
         (mouse_x + line_length, mouse_y)],
        fill='red',
        width=2
    )
    # 垂直线
    draw.line(
        [(mouse_x, mouse_y - line_length),
         (mouse_x, mouse_y + line_length)],
        fill='red',
        width=2
    )
    
    # 在鼠标位置附近标注坐标（小字，不遮挡太多）
    try:
        from PIL import ImageFont
        import platform
        font = None
        if platform.system() == "Windows":
            font_paths = [
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/arial.ttf",
            ]
            for path in font_paths:
                try:
                    font = ImageFont.truetype(path, 10)
                    break
                except:
                    continue
        if font is None:
            font = ImageFont.load_default()
        coord_text = f"({mouse_x}, {mouse_y})"
        # 在鼠标位置右下方显示坐标
        draw.text((mouse_x + 20, mouse_y + 20), coord_text, fill='red', font=font)
    except:
        pass
    
    # 将图片转换为字节流
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return Image(data=img_byte_arr, format="png")

@mcp.tool()
def move_mouse(x: int, y: int) -> str:
    """
    将鼠标移动到指定的 (x, y) 坐标。
    """
    try:
        pyautogui.moveTo(x, y, duration=0.5) # duration 让移动更像人类，也更容易调试
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {str(e)}"

@mcp.tool()
def click(x: int = None, y: int = None, double_click: bool = False, verify: bool = False) -> str:
    """
    在指定坐标点击鼠标左键。
    如果未提供 x, y，则在当前位置点击。
    
    Args:
        x: 点击的X坐标
        y: 点击的Y坐标
        double_click: 是否双击
        verify: 如果为True，点击后会返回当前鼠标位置，用于验证点击是否准确
    """
    try:
        if x is not None and y is not None:
            pyautogui.moveTo(x, y)
            actual_x, actual_y = pyautogui.position()
        
        if double_click:
            pyautogui.doubleClick()
            action = "Double clicked"
        else:
            pyautogui.click()
            action = "Clicked"
        
        result = f"{action} at ({x if x else 'current'}, {y if y else 'current'})"
        
        # 如果启用验证，返回实际点击位置
        if verify and x is not None and y is not None:
            result += f"\n实际鼠标位置: ({actual_x}, {actual_y})"
            if abs(actual_x - x) > 5 or abs(actual_y - y) > 5:
                result += f"\n警告: 实际位置与目标位置偏差较大！"
            
        return result
    except Exception as e:
        return f"Error clicking: {str(e)}"

@mcp.tool()
def type_text(text: str, enter: bool = True) -> str:
    """
    在当前焦点位置输入文本。
    enter: 输入完成后是否按下回车键。
    """
    try:
        pyautogui.write(text, interval=0.05) # interval 模拟打字速度
        if enter:
            pyautogui.press('enter')
        return f"Typed: {text}"
    except Exception as e:
        return f"Error typing: {str(e)}"

@mcp.tool()
def scroll(amount: int) -> str:
    """
    滚动屏幕。正数向上滚动，负数向下滚动。
    """
    pyautogui.scroll(amount)
    return f"Scrolled by {amount}"

@mcp.tool()
def press_key(key: str) -> str:
    """
    按下指定的键盘按键。
    常用按键：'win' (Windows键), 'enter', 'esc', 'tab', 'space', 'ctrl', 'alt', 'shift' 等。
    组合键示例：'ctrl+c', 'alt+tab', 'win+r' 等。
    """
    try:
        # 如果是组合键（包含+号），使用 hotkey 函数
        if '+' in key:
            keys = key.split('+')
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(key)
        return f"Pressed key: {key}"
    except Exception as e:
        return f"Error pressing key: {str(e)}"

if __name__ == "__main__":
    # 运行服务
    mcp.run()