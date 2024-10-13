import pyautogui
import cv2
import numpy as np

# 数字区域的坐标和大小
NUMBER_REGION = (229, 347, 190, 50)  # 示例坐标，调整为你游戏的实际坐标

# 截取该区域
screenshot = pyautogui.screenshot(region=NUMBER_REGION)
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# 显示截取的区域
cv2.imshow("Captured Number Region", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()