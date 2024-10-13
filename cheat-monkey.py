import cv2
import pytesseract
import pyautogui
import numpy as np
import time
import keyboard  # 用于监听键盘事件

# Tesseract的安装路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 游戏窗口的区域 (请调整以适应实际情况)
GAME_REGION = (240, 320, 300, 110)   # 左上角坐标 (x, y) 和窗口的宽度和高度
NUMBER_REGION = (240, 320, 300, 110)  # 数字区域坐标 (x, y, 宽, 高)

def get_numbers_from_image(image):
    """从游戏窗口截图中提取数字"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化处理，增强数字识别效果
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 使用OCR提取文本
    text = pytesseract.image_to_string(binary_image, config='--psm 7')
    return text


def extract_valid_numbers(text):
    """过滤无效字符并提取有效数字"""
    filtered_text = ''.join([ch if ch.isdigit() or ch in ['?', ' '] else '' for ch in text])

    # 尝试基于"?"拆分数字
    if '?' in filtered_text:
        parts = filtered_text.split('?')
        if len(parts) == 2:
            try:
                left_num = int(parts[0].strip())
                right_num = int(parts[1].strip())
                return left_num, right_num
            except ValueError:
                return None, None
    else:
        # 使用空格作为分隔符提取左右两边的数字
        parts = filtered_text.split()
        if len(parts) >= 2:
            try:
                left_num = int(parts[0].strip())
                right_num = int(parts[1].strip())
                return left_num, right_num
            except ValueError:
                return None, None
    return None, None


def compare_and_draw(left_num, right_num):
    """根据比较结果，在屏幕上画出'<'或'>'形状"""
    x, y = 384, 824  # 固定的绘图起点

    if left_num > right_num:
        print(f"{left_num} > {right_num}: 绘制 '>'")
        pyautogui.moveTo(x, y)
        pyautogui.dragRel(50, 0, duration=0.01)  # 画右边线
        pyautogui.dragRel(-25, 50, duration=0.01)  # 画下边线
        pyautogui.dragRel(-25, -50, duration=0.01)  # 画左边线
    elif right_num > left_num:
        print(f"{left_num} < {right_num}: 绘制 '<'")
        pyautogui.moveTo(x, y)
        pyautogui.dragRel(-50, 0, duration=0.01)  # 画左边线
        pyautogui.dragRel(25, 50, duration=0.01)  # 画下边线
        pyautogui.dragRel(25, -50, duration=0.01)  # 画右边线
    else:
        print(f"{left_num} = {right_num}: 忽略相等情况")


def main():
    while True:
        # 检查是否按下了结束快捷键
        if keyboard.is_pressed('s'):
            print("检测到 'S' 键，程序退出")
            break

        # 截取游戏窗口
        screenshot = pyautogui.screenshot(region=GAME_REGION)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 从截图中提取数字
        numbers_text = get_numbers_from_image(screenshot)
        print(f"OCR提取的文本: {numbers_text}")

        # 过滤并尝试提取有效的数字
        left_num, right_num = extract_valid_numbers(numbers_text)
        if left_num is not None and right_num is not None:
            # 根据数字大小，执行鼠标绘图操作
            compare_and_draw(left_num, right_num)
        else:
            print("无效的数字提取或未能成功检测到数字，等待下一次判断")

        # 暂停一下，防止过快执行
        time.sleep(0.4)


if __name__ == "__main__":
    print("程序已启动，按 'S' 键可退出程序")
    main()