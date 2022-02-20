import cv2
import numpy as np
import win32ui
from PIL import Image
import win32gui, win32api, win32con
import time
import os
import random
from datetime import datetime


# для работы с api просто подключить через import api
# api.pyc должен быть в одной папке со скриптом
# winname - имя окна, пример: 'BlueStacks';  sdevice - '127.0.0.1:5555' - ip виртуалки
# dev = 0 или 1 // активирует логи  качества возвращаемого template.png
# x, y = api.imgsearch('./img/', 'template.png', 0.94, winname, dev).img_search() # Поиск шаблона и возврат координат
# .img_search(0) - возвращает (X, Y); .img_search(1) - возвращает [(X, Y), 'имя_найденого_шаблона.png']
# api.core(x, y, winname).click(0.3) # клик в окне по координатам (x, y), (0.3) - время нажатия
# api.core(x, y, winname).arrow_up(2) # кнопка UP, (2) - время нажатия
# api.core(x, y, winname).esc(0.4) # кнопка ESC, 0.4 - время нажатия
# api.core(x, y, winname).adb_tap(sdevice, rx=0, ry=0, tsleep=1, input='tap') # варианты нажатий через ADB input: tap, long_tap, swipe
#  ( rx=0, ry=0 ) смещение по x, y в пикселях
# BSIP - IP окна
# api.core(x, y, winname).adb_tap(bsip, 0, 0, 0, 'tap') # winname - имя окна,bswinname - IP:PORT
# api.core(x, y, winname).adb_tap(bsip, 0, 0, 1, 'long_tap')
# api.core(x, y, winname).adb_tap(bsip, 0, 350, 3, 'swipe')

#tap
#tap_swipe
#long_tap
#swipe
#touchscreen_swipe
#touchscreen_tap


#import api

#def example_func():
#    pic = ['star.png']
#    folder = './img/'
#    b = api.imgsearch(folder, pic, 0.94, winname, 0).img_search(0)
#    if b[0] != -1:
#        x, y = b
#        api.core(x, y, winname).adb_tap(bswinname, 30, 0, 0, 'tap')  # клик по ip окна(через adb)
#        #api.core(x, y, winname).click(0.3) # клик в окне по координатам
#        time.sleep(10)
#    else:
#        print('Not found img')

# folder = './img/'
# point1_pic = ['star.png']
# print(api.imgsearch(folder, point1_pic, 0.94, winname, 2).img_search(0)) #(..., winname, 2 ) Делает криншот окна
# Making screenshot
# (818, 645)
# print(api.imgsearch(folder, point1_pic, 0.94, winname, 0).img_search(1)) # debug режим
# ./img_tiron/star.png BindRes:  0.94 Max_Val:  0.9771263003349304 Location:  818.0 645.0
# (818, 645)
# print(api.imgsearch(folder, point1_pic, 0.94, winname, 0).img_search(2)) # возвращает XY и и шаблон который нашло
# ((818, 645), 'star.png')



adb_folder = '/adb/adb'


class core:
    def __init__(self, my_x, my_y, my_winname):
        self.winname = my_winname
        self.x = my_x
        self.y = my_y

    def esc(self, stime):
        hwnd = win32gui.FindWindow(None, self.winname)
        #win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
        time.sleep(.5)  # Without this delay, inputs are not executing in my case
        hWnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
        win32api.SendMessage(hWnd1, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
        time.sleep(stime)
        win32api.SendMessage(hWnd1, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)

    # Кнопка Arrow up
    def arrow_up(self, stime):
        hwnd = win32gui.FindWindow(None, self.winname)
        hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
        hwndChild2 = win32gui.GetWindow(hwndChild, win32con.GW_CHILD)
        win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
        time.sleep(.5)  # Without this delay, inputs are not executing in my case
        win32api.SendMessage(hwndChild2, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
        time.sleep(stime)
        win32api.SendMessage(hwndChild2, win32con.WM_KEYUP, win32con.VK_UP, 0)

    # Клик мышки // Долгий клик мышки нужно увеличить sleep
    def click(self, stime):
        hwnd = win32gui.FindWindow(None, self.winname)
        #win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
        x = self.x
        y = self.y
        time.sleep(.5)  # Without this delay, inputs are not executing in my case
        hWnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(stime)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

    def kill_app(self, sdevice):
        print("Закрываю игру")
        os.system(adb_folder + " -s " + str(sdevice) + " shell am force-stop com.jagex.runescape.android")

    def run_app(self, sdevice):
        print("Запускаю новую игру")
        os.system(adb_folder + " -s " + str(sdevice) + " shell am start com.jagex.runescape.android/com.jagex.android.MainActivity")

    def adb_tap(self, sdevice, rx=0, ry=0, tsleep=1, input='tap'):

        if input == 'tap':
            os.system(adb_folder + " -s " + str(sdevice) + " shell input tap "
                      + str(self.x + rx)
                      + ' '
                      + str(self.y + ry))
        elif input == 'tap_swipe':
            rtime = random.randint(15, 30)
            r = random.randint(0, 2)
            os.system(adb_folder + " -s " + str(sdevice) + " shell input swipe "
                      + str(self.x + rx) + ' '
                      + str(self.y + ry) + ' '
                      + str(self.x + r + rx) + ' '
                      + str(self.y + r + ry) + ' '
                      + str(rtime))
        elif input == 'long_tap':
            os.system(adb_folder + " -s " + str(sdevice) + " shell input swipe "
                      + str(self.x) + ' '
                      + str(self.y) + ' '
                      + str(self.x + rx) + ' '
                      + str(self.y + ry) + ' '
                      + str(tsleep*1000))
        elif input == 'swipe':
            os.system(adb_folder + " -s " + str(sdevice) + " shell input swipe "
                      + str(self.x) + ' '
                      + str(self.y) + ' '
                      + str(self.x + rx) + ' '
                      + str(self.y + ry) + ' '
                      + str(tsleep*1000))
        elif input == 'touchscreen_swipe':
            r = random.randint(-2, 2)
            rtime = random.randint(16, 50)
            os.system(adb_folder + " -s " + str(sdevice) + " shell input touchscreen swipe "
                      + str(self.x) + ' '
                      + str(self.y) + ' '
                      + str(self.x + r + rx) + ' '
                      + str(self.y + r + ry) + ' '
                      + str(rtime))
        elif input == 'touchscreen_tap':
            r = random.randint(-2, 2)
            os.system(adb_folder + " -s " + str(sdevice) + " shell input touchscreen tap "
                      + str(self.x + r) + ' '
                      + str(self.y + r))

def real_time():
    dateTimeObj = datetime.now()
    timeStr = dateTimeObj.strftime("%H:%M:%S")
    t = ' ' + timeStr + ' '
    return t

class imgsearch:
    def __init__(self, folder, template, res, winname, dev):
        self.my_folder = folder
        self.my_template = template
        self.my_res = res
        self.my_winname = winname
        self.my_dev = dev



    def custom_screen(self, pw, ph, pw_x, pw_y, sdev=0):
        hwnd = win32gui.FindWindow(None, self.my_winname)

        #print(pw, ph, pw_x, pw_y)
        hwnddc = win32gui.GetWindowDC(hwnd)
        mfcdc = win32ui.CreateDCFromHandle(hwnddc)
        savedc = mfcdc.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()

        saveBitMap.CreateCompatibleBitmap(mfcdc, pw, ph)
        savedc.SelectObject(saveBitMap)
        savedc.BitBlt((0, 0), (pw, ph), mfcdc, (pw_x, pw_y), win32con.SRCCOPY)

        bmpstr = saveBitMap.GetBitmapBits(True)

        bmp = Image.frombytes('RGB', (saveBitMap.GetInfo()['bmWidth'], saveBitMap.GetInfo()['bmHeight']), bmpstr, 'raw',
                              'BGRX')

        win32gui.DeleteObject(saveBitMap.GetHandle())
        savedc.DeleteDC()
        mfcdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnddc)
        img = np.array(bmp)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print('Making screenshot')
        #cv2.imwrite('screenshot.png', img)
        #cv2.imshow("Result:", img)
        #cv2.waitKey(0)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        for x in self.my_template:
            time.sleep(.7)
            template = cv2.imread(self.my_folder + x)
            template1 = x
            template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
            w, h = template.shape[:-1]
            res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if sdev == 1:
                print(real_time(), ' ',self.my_folder + x, 'BindRes: ', self.my_res, 'Max_Val: ', max_val, 'Location: ',
                      (max_loc[0] + (h / 2)), (max_loc[1] + (w / 2)))
            if max_val >= self.my_res:
                x, y = max_loc
                xy = round(x + (h / 2)), round(y + (w / 2))
                return xy, template1
        else:
            return [-1, -1]

    def window_capture(self):
        hwnd = win32gui.FindWindow(None, self.my_winname)
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
        if self.my_dev == 2:
            print('Making screenshot')
            cv2.imwrite('screenshot.png', img)
        # cv2.imshow("Result:", img)
        # cv2.waitKey(0)
        return img

    def img_search(self, sdev=0):
        img_screen = self.window_capture()
        img_gray = cv2.cvtColor(img_screen, cv2.COLOR_RGB2GRAY)
        for x in self.my_template:
            time.sleep(.5)
            template = cv2.imread(self.my_folder + x)
            template1 = x
            template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
            w, h = template.shape[:-1]
            res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if sdev == 1:
                print(self.my_folder + x, 'BindRes: ', self.my_res, 'Max_Val: ', max_val, 'Location: ', (max_loc[0]+(h / 2)), (max_loc[1]+ (w / 2)) )
            if max_val >= self.my_res:
                x, y = max_loc
                xy = round(x + (h / 2)), round(y + (w / 2))
                return xy, template1
        else:
            return [-1, -1]


