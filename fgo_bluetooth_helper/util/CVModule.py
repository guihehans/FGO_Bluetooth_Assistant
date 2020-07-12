import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con, win32api
import sys
from fgo_bluetooth_helper.util import config_6s

output_dir = config_6s.output_dir


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
    width = int((right - left))
    height = int((bot - top))
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
    cv.imwrite(output_dir + 'test.jpg', cropped)
    win32gui.DeleteObject(saveBitMap.GetHandle())  # 释放内存
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    # return saved screen
    return cropped


def match_template(filename, show_switch=False, threshold=0.85):
    """
    given the template filename, try to find if the template matches the screen capture.
    return found or not flag, and the center coordination of matched template location.

    :param filename: template name. e.g, "AP_COVER"
    :param show_switch: control flag for show found img or not. default set to False to now show.
    :param threshold: the err threshold
    :return: found or not flag and center location.
    """
    template_dir = config_6s.template_dir + filename + '.jpg'
    # get the screen captured image
    img = window_capture()
    # read template
    template_img = cv.imread(template_dir)
    result = cv.matchTemplate(img, template_img, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # 当图片中有与模板匹配度超过threshold的部分时：
    if max_val > threshold:
        # mark center location. return Found=True and center location
        # in method cv.TM_CCOEFF_NORMED, max_loc[0] is the top left point location
        top_left = max_loc
        template_width = template_img.shape[1]
        template_height = template_img.shape[0]
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        center_loc = (top_left[0] + int(template_width / 2), top_left[1] + int(template_height / 2))

        # if show_switch is Ture, circle the found template.
        if show_switch:
            cv.circle(img, center_loc, 10, (0, 255, 255), -1)
            cv.rectangle(img, max_loc, bottom_right, (0, 0, 255), 3)
            cv.namedWindow('FGO_MatchResult', cv.WINDOW_KEEPRATIO)
            cv.imshow("FGO_MatchResult", img)
            # 显示结果1秒钟
            k = cv.waitKey(1000)
            if k == -1:
                cv.destroyAllWindows()

        return True, center_loc
    else:
        return False, 0


if __name__ == '__main__':
    result = match_template("drag_bar", show_switch=False)
    print(result)
