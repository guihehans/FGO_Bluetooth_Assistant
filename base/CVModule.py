import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con, win32api
import sys


def window_capture():
    """
    capture the window image from iphone sent through Airplayer.

    :return:
    """
    hwnd = win32gui.FindWindow("CHWindow", None)  # get window handler. the window Handler name is CHWindow
    # 根据窗口句柄获取窗口的设备上下文DC（Device Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, filename)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    # img = cv.imread(filename)
    # 截取出ios屏幕区域
    cropped = img[37:height - 1, 1:width - 1]  # 裁剪坐标为[y0:y1, x0:x1]
    cv.imwrite('test.jpg', cropped)
    win32gui.DeleteObject(saveBitMap.GetHandle())  # 释放内存
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return cropped

def test_window():
    print("test")
    window_capture()
class CVModule:
    pass


if __name__ == '__main__':
    # Load an color image in grayscale
    # path = r'..\Template\Add_friend.jpg'
    # img = cv.imread(path, 0)
    # cv.imshow('image', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    test_window()
