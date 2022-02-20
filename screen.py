import cv2
import numpy as np
import win32ui
from PIL import Image
import win32gui, win32api, win32con
my_winname = 'BlueStacks'
my_dev = 2
def window_capture():
    hwnd = win32gui.FindWindow(None, my_winname)
    window_rect = win32gui.GetWindowRect(hwnd)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]
    border_pixels = 3
    titlebar_pixels = 42
    w = w - (border_pixels * 2)
    h = h - titlebar_pixels - border_pixels
    cropped_x = border_pixels
    cropped_y = titlebar_pixels

    hwnddc = win32gui.GetWindowDC(hwnd)
    mfcdc = win32ui.CreateDCFromHandle(hwnddc)
    savedc = mfcdc.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()

    saveBitMap.CreateCompatibleBitmap(mfcdc, w, h)
    savedc.SelectObject(saveBitMap)
    savedc.BitBlt((0, 0), (w, h), mfcdc, (cropped_x, cropped_y), win32con.SRCCOPY)

    bmpstr = saveBitMap.GetBitmapBits(True)

    bmp = Image.frombytes('RGB', (saveBitMap.GetInfo()['bmWidth'], saveBitMap.GetInfo()['bmHeight']), bmpstr, 'raw',
                          'BGRX')

    win32gui.DeleteObject(saveBitMap.GetHandle())
    savedc.DeleteDC()
    mfcdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnddc)
    img = np.array(bmp)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if my_dev == 2:
        print('Making screenshot')
        cv2.imwrite('screenshot.png', img)
    # cv2.imshow("Result:", img)
    # cv2.waitKey(0)
    return img

window_capture()