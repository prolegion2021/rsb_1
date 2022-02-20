import random
import win32gui
import time
import api
import argparse
from configparser import ConfigParser
import ast
from datetime import datetime
from threading import Thread
import os

parser = argparse.ArgumentParser(description='Пробная версия запуска')
parser.add_argument(
    '--title',
    type=str,
    default=''
)

my_namespace = parser.parse_args()
name = my_namespace.title

# winname = 'BlueStacks'
winname = name
file = 'config.ini'
config = ConfigParser()
config.read(file)

bswinname = ast.literal_eval(config[winname]['ip'])
bstimer = ast.literal_eval(config[winname]['close_timer1'])
bstimer1 = ast.literal_eval(config[winname]['close_timer2'])
bstimer2 = ast.literal_eval(config[winname]['restart_timer1'])
bstimer3 = ast.literal_eval(config[winname]['restart_timer2'])
rserver = ast.literal_eval(config[winname]['random_server'])
typebot = ast.literal_eval(config[winname]['typebot'])
eventxp = ast.literal_eval(config[winname]['event_xp'])

global_adb_folder = ast.literal_eval(config['Global_settings']['adb_folder'])
g_dev = ast.literal_eval(config['Global_settings']['global_dev'])
check_folder = ast.literal_eval(config['Global_settings']['folder'])
gcheck = ast.literal_eval(config['Global_settings']['gamecheck'])
gcheck_res = ast.literal_eval(config['Global_settings']['gamecheck_res'])

inproc_folder = ast.literal_eval(config['Global_settings']['in_proc_f'])
inprocimg = ast.literal_eval(config['Global_settings']['in_proc'])
inprocimg_res = ast.literal_eval(config['Global_settings']['inp_roc_res'])

confirm = ast.literal_eval(config['Global_settings']['confirm'])
confirm_fold = ast.literal_eval(config['Global_settings']['confirm_fold'])
confirm_res = ast.literal_eval(config['Global_settings']['confirm_res'])

invfull = ast.literal_eval(config['Global_settings']['inv_full'])
invfull_fold = ast.literal_eval(config['Global_settings']['inv_full_fold'])
invfull_res = ast.literal_eval(config['Global_settings']['inv_full_res'])


sf1_folder = ast.literal_eval(config['room_1']['folder'])
sf1_artefact = ast.literal_eval(config['room_1']['artefact'])
sf1_artefact_res = ast.literal_eval(config['room_1']['artefact_res'])
sf1_storage = ast.literal_eval(config['room_1']['storage'])
sf1_storage_res = ast.literal_eval(config['room_1']['storage_res'])
sf1_ore = ast.literal_eval(config['room_1']['ore'])
sf1_ore_res = ast.literal_eval(config['room_1']['ore_res'])


sf2_folder = ast.literal_eval(config['room_2']['folder'])
sf2_artefact = ast.literal_eval(config['room_2']['artefact'])
sf2_artefact_res = ast.literal_eval(config['room_2']['artefact_res'])
sf2_storage = ast.literal_eval(config['room_2']['storage'])
sf2_storage_res = ast.literal_eval(config['room_2']['storage_res'])
sf2_ore = ast.literal_eval(config['room_2']['ore'])
sf2_ore_res = ast.literal_eval(config['room_2']['ore_res'])
sf2_apoint = ast.literal_eval(config['room_2']['point'])
sf2_apoint_res = ast.literal_eval(config['room_2']['point_res'])

tiron_folder = ast.literal_eval(config['Third_iron']['folder'])
tiron_storage = ast.literal_eval(config['Third_iron']['storage'])
tiron_storage_folder = ast.literal_eval(config['Third_iron']['storage_folder'])
tiron_storage_res = ast.literal_eval(config['Third_iron']['storage_res'])
tiron_ore = ast.literal_eval(config['Third_iron']['ore'])
tiron_ore_res = ast.literal_eval(config['Third_iron']['ore_res'])

bpoint = ast.literal_eval(config['iron_tyrian']['bpoint'])
bpoint_folder = ast.literal_eval(config['iron_tyrian']['bpoint_folder'])
bpoint_res = ast.literal_eval(config['iron_tyrian']['bpoint_res'])

tyrian_folder = ast.literal_eval(config['Tyrian']['ore_folder'])
tyrian_ore = ast.literal_eval(config['Tyrian']['ore'])
tyrian_ore_res = ast.literal_eval(config['Tyrian']['ore_res'])
tyrian_storage_folder = ast.literal_eval(config['Tyrian']['storage_folder'])
tyrian_storage = ast.literal_eval(config['Tyrian']['storage'])
tyrian_storage_res = ast.literal_eval(config['Tyrian']['storage_res'])
dang_enter = ast.literal_eval(config['Tyrian']['dang_enter'])
dang_enter_res = ast.literal_eval(config['Tyrian']['dang_enter_res'])
dang_in = ast.literal_eval(config['Tyrian']['dang_in'])
dang_in_res = ast.literal_eval(config['Tyrian']['dang_in_res'])
bankp = ast.literal_eval(config['Tyrian']['bankp'])
bankp_res = ast.literal_eval(config['Tyrian']['bankp_res'])


hwnd = win32gui.FindWindow(None, winname)
os.system(global_adb_folder + " connect " + str(bswinname))
# 1097 650
# 1091 647

camera = 0
player_pos = 0
in_game = 0
info = 0
stop = False
timer = 0
drop_count = 0
inv = 1
orecheck = 0



def real_time():
    dateTimeObj = datetime.now()
    timeStr = dateTimeObj.strftime("%H:%M:%S")
    t = '[' + winname + ']' + ' ' + timeStr + ' '
    return t


def timer_check():
    global timer_restart, need_close, info, stop
    i = 0
    while not stop:
        time.sleep(1)
        i = i + 1
        info = i
    else:
        info = 0
        timer_off()


def timer_off():
    global timer
    timer = random.randint(bstimer, bstimer1)


def camera_to_default():
    global camera
    rs = random.randint(300, 500)
    rx = random.randint(300, 600)
    ry = random.randint(100, 200)
    rtime = random.randint(3, 5)
    api.core(rx, ry, winname).adb_tap(bswinname, 0, rs, rtime, 'swipe')
    time.sleep(3)
    camera = 1


def game_check():
    global in_game, camera, player_pos, inv, orecheck
    b = api.imgsearch(check_folder, gcheck, gcheck_res, winname, 0).img_search(g_dev)
    img = b[1]
    if img == 'sword.png':
        print(real_time() + 'Мы в игре')
        in_game = 2
    elif img == 'loot.png':
        x, y = b[0]
        ry = random.randint(-5, 5)
        rx = random.randint(-5, 5)
        api.core(x+rx, y + ry, winname).adb_tap(bswinname, 205, 0, 0, 'tap_swipe')
        print(real_time() + 'Закрываю окно !!!')
    elif img == 'lobby_star.png':
        in_game = 0
        camera = 0
        player_pos = 0
        orecheck = 0
        inv = 1
        print(real_time() + 'Мы в Lobby')
        x, y = b[0]
        rx = random.randint(1, 10)
        ry = random.randint(-5, 5)
        # +50 (первый) +126(второй) +210(третий)
        rs = 50
        if rserver == 1:
            rs = random.sample((50, 126, 210), 1)
            rs = rs[0]
        api.core(x + rs + rx, y, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(5)
    elif img == 'play_welcome.png':
        in_game = 0
        camera = 0
        player_pos = 0
        orecheck = 0
        inv = 1
        print(real_time() + 'Страница авторизации')
        x, y = b[0]
        ry = random.randint(30, 60)
        rx = random.randint(20, 60)
        api.core(x + rx, y + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        print(real_time() + 'Пробую войти !!!')
        time.sleep(5)
    elif img == 'event_exit.png':
        in_game = 0
        camera = 0
        player_pos = 0
        orecheck = 0
        inv = 1
        print(real_time() + 'Надо закрыть Окно ивента')

        reward = ['claim_reward.png']
        a = api.imgsearch('./img/check/', reward, 0.92, winname, 0).img_search(g_dev)
        x1, y1 = a[0]
        ry = random.randint(-5, 5)
        rx = random.randint(-50, 50)
        api.core(x1 + rx, y1 + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(1)

        x, y = b[0]
        ry = random.randint(-5, 5)
        api.core(x + ry, y + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        print(real_time() + 'Пробую закрыть !!!')
        time.sleep(3)
    else:
        in_game = 0
        camera = 0
        player_pos = 0
        orecheck = 0
        inv = 1


def confirm_destroy():
    global player_pos
    b = api.imgsearch(confirm_fold, confirm, confirm_res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        x, y = b[0]
        r = random.randint(-2, 2)
        rx = random.randint(-15, 15)
        api.core(x+rx, y+r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(2)
    else:
        print('Not found img confirm_destroy')


def drop(folder, drop_img, res=0.9):
    global drop_count
    drop_count += 1
    if drop_count >= 10:
        b = api.imgsearch(folder, drop_img, res, winname, 0).custom_screen(350, 690, 865, 54, g_dev)
        drop_count = 0
    else:
        drop = ['drop_0.png']
        b = api.imgsearch(folder, drop, res, winname, 0).custom_screen(350, 690, 865, 54, g_dev)

    if b[0] != -1 and b[1] == 'drop_art_0.png':
        print('Нашел дроп', b[1])
        r = random.randint(-3, 3)
        rx = random.randint(-490, -450)
        ry = random.randint(-100, 30)
        rt = random.randint(1, 2)
        x, y = b[0]
        api.core(x+862 + r, y+12 + r, winname).adb_tap(bswinname, rx, ry, rt, 'swipe')
        time.sleep(3)
        drop_count = 0
        confirm_destroy()

    elif b[0] != -1 and b[1] == 'drop_art_1.png':
        print('Нашел дроп', b[1])
        r = random.randint(-3, 3)
        rx = random.randint(-490, -450)
        ry = random.randint(-100, 30)
        rt = random.randint(1, 2)
        x, y = b[0]
        api.core(x+862 + r, y+12 + r, winname).adb_tap(bswinname, rx, ry, rt, 'swipe')
        time.sleep(3)
        drop_count = 0
        confirm_destroy()

    elif b[0] != -1 and b[1] == 'drop_clue_scroll.png':
        print('Нашел дроп', b[1])
        r = random.randint(-3, 3)
        rx = random.randint(-490, -450)
        ry = random.randint(-100, 30)
        rt = random.randint(1, 2)
        x, y = b[0]
        api.core(x+862 + r, y+12 + r, winname).adb_tap(bswinname, rx, ry, rt, 'swipe')
        time.sleep(3)
        drop_count = 0
        confirm_destroy()

    elif b[0] != -1:
        print('Нашел дроп', b[1])
        r = random.randint(-3, 3)
        rx = random.randint(-490, -450)
        ry = random.randint(-100, 30)
        rt = random.randint(1, 2)
        x, y = b[0]
        api.core(x+862 + r, y+12 + r, winname).adb_tap(bswinname, rx, ry, rt, 'swipe')
        time.sleep(2)
    else:
        print('Ничего не нашел')
        time.sleep(2)


def in_proc():
    global orecheck
    b = api.imgsearch(inproc_folder, inprocimg, inprocimg_res, winname, 0).custom_screen(70, 60, 605, 140, g_dev)
    if orecheck == 0:
        print('Запуск потока проверки инвентаря')
        thread_inv = Thread(target=ore_check_fast)
        thread_inv.start()
        orecheck = 1
    if b[0] != -1:
        if typebot == 1:
            drop(sf1_folder, sf1_artefact, sf1_artefact_res)
        elif typebot == 2:
            drop(sf2_folder, sf2_artefact, sf2_artefact_res)
        return False
    else:
        return True


def ore_check_fast():
    global inv, orecheck, player_pos, in_game
    while True:
        orecheck = 1
        time.sleep(1)
        b = api.imgsearch(invfull_fold, invfull, invfull_res, winname, 0).custom_screen(250, 30, 515, 260, g_dev)
        if b[0] != -1:
            print(real_time() + 'Заполнен, пора валить')
            inv = 1
            player_pos = 0
            return False


def sf_storage(folder, img, sleep, res=0.8):
    global inv, orecheck
    b = api.imgsearch(folder, img, res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        x, y = b[0]
        r = random.randint(-2, 2)
        api.core(x+r, y+r, winname).adb_tap(bswinname, -3, -3, 0, 'tap_swipe')
        inv = 0
        orecheck = 0
        time.sleep(sleep)
        if typebot == 1:
            drop(sf1_folder, sf1_artefact, sf1_artefact_res)
        elif typebot == 2:
            drop(sf2_folder, sf2_artefact, sf2_artefact_res)
    else:
        if typebot == 1:
            ore_mining(sf1_folder, sf1_ore, sf1_ore_res)
        print('Not found img storage')


def ore_mining(folder, img, res=0.85):
    if in_proc():
        b = api.imgsearch(folder, img, res, winname, 0).img_search(g_dev)
        if b[0] != -1:
            x, y = b[0]
            r = random.randint(-3, 3)
            api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
            if typebot == 1:
                drop(sf1_folder, sf1_artefact, sf1_artefact_res)
            elif typebot == 2:
                drop(sf2_folder, sf2_artefact, sf2_artefact_res)
            time.sleep(5)


def to_mining():
    global inv, orecheck
    b = api.imgsearch(sf2_folder, sf2_apoint, sf2_apoint_res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        rtime = random.randint(10, 12)
        x, y = b[0]
        r = random.randint(-2, 2)
        api.core(x+r, y+r, winname).adb_tap(bswinname, 2, 48, 0, 'tap_swipe')
        inv = 0
        orecheck = 0
        time.sleep(rtime)
    else:
        to_mining()
        print('Not found img storage')


def to_storage():
    global inv
    b = api.imgsearch(sf2_folder, sf2_apoint, sf2_apoint_res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        rtime = random.randint(10, 12)
        x, y = b[0]
        r = random.randint(-2, 2)
        api.core(x+r, y+r, winname).adb_tap(bswinname, 94, 0, 0, 'tap_swipe')
        time.sleep(rtime)
    else:
        to_storage()
        print('Not found img storage')


def event_check():
    global eventxp
    while True:
        time.sleep(1)
        ivent_img = ['exp_clock.png']
        b = api.imgsearch('./img/check/', ivent_img, 0.9, winname, 0).img_search(g_dev)
        if b[0] != -1:
            rtime = random.randint(2, 3)
            x, y = b[0]
            r = random.randint(-2, 2)
            api.core(x + r, y + r, winname).adb_tap(bswinname, 3, -35, 0, 'tap_swipe')
            eventxp = 0
            time.sleep(rtime)
            return False


########################### Third Age Iron - Type 3 ####################################


def tbank(x1, y1, res, rtime1=11, rtime2=13):
    #bank_point = ['bank_point_1.png', 'bank_point_0.png']

    b = api.imgsearch(bpoint_folder, bpoint, bpoint_res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        rtime = random.randint(rtime1, rtime2)
        x, y = b[0]
        r = random.randint(-2, 2)
        api.core(x + r, y + r, winname).adb_tap(bswinname, x1, y1, 0, 'tap_swipe')
        time.sleep(rtime)


def third_ore_mining(folder, img, res):
    b = api.imgsearch(folder, img, res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        x, y = b[0]
        r = random.randint(-3, 3)
        api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        r = random.randint(15, 20)
        time.sleep(r)


####################################### Tyrian botype 4 ##################################################


def tyrian_bank_point():
    global player_pos
    b = api.imgsearch(tyrian_folder, bankp, bankp_res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        rtime = random.randint(12, 13)
        x, y = b[0]
        r = random.randint(-2, 2)
        api.core(x + r, y + r, winname).adb_tap(bswinname, 92, -21, 0, 'tap')
        time.sleep(rtime)
        player_pos = 2
    else:
        player_pos = 0


def enter_dang():
    global player_pos, inv
    b = api.imgsearch(tyrian_folder, dang_enter, dang_enter_res, winname, 0).img_search(g_dev)
    if b[0] != -1:
        x, y = b[0]
        r = random.randint(-2, 2)
        api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        player_pos = 4
        time.sleep(3)
    else:
        player_pos = 0
        inv = 1


def tmining_point():
    global player_pos
    i = 0
    while i <= 10:
        time.sleep(1)
        b = api.imgsearch(tyrian_folder, dang_in, dang_in_res, winname, 0).img_search(g_dev)
        i += 1
        if b[0] != -1:
            print(real_time() + 'Нашел точку копки ...')
            x, y = b[0]
            r = random.randint(-2, 2)
            api.core(x + r, y + r, winname).adb_tap(bswinname, -16, 0, 0, 'tap_swipe')
            time.sleep(random.randint(14, 15))
            player_pos = 5
            break


def teleport_book():
    global player_pos
    bank_point = ['sword.png']
    b = api.imgsearch('./img/check/', bank_point, 0.9, winname, 0).img_search(g_dev)
    if b[0] != -1:
        x, y = b[0]
        r = random.randint(-15, 15)
        api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(1)
        i = 0
        while i <= 5:
            time.sleep(1)
            mining_point = ['book.png']
            b = api.imgsearch('./img/tyrian/', mining_point, 0.92, winname, 0).img_search(g_dev)
            i += 1
            if b[0] != -1:
                print(real_time() + 'Нашел книгу ...')
                x, y = b[0]
                r = random.randint(-7, 7)
                api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
                time.sleep(3)
                i = 0
                while i <= 10:
                    time.sleep(1)
                    mining_point = ['sword.png']
                    b = api.imgsearch('./img/check/', mining_point, 0.92, winname, 0).img_search(g_dev)
                    i += 1
                    if b[0] != -1:
                        print(real_time() + 'Проверка после телепорта ...')
                        x, y = b[0]
                        r = random.randint(-15, 15)
                        api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
                        player_pos = 1
                        time.sleep(3)
                        break
                break


def protean_in_proc():
    inproc = ['craft_check.png']
    b = api.imgsearch('./img/', inproc, 0.94, winname, 0).img_search(0)
    if b[0] != -1:
        return False
    else:
        return True


def protean(folder, img, res):
    if protean_in_proc():
        r = random.randint(-25, 25)
        api.core(905 + r, 224 + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(3)
        b = api.imgsearch(folder, img, res, winname, 0).img_search(0)
        if b[0] != -1:
            print(real_time() + 'Стартую крафт')
            x, y = b[0]
            rx = random.randint(-70, 70)
            ry = random.randint(-20, 20)
            api.core(x + rx, y + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
            time.sleep(4)


def new_storage(folder, img, res):
    global inv, orecheck, player_pos
    b = api.imgsearch(folder, img, res, winname, 0).img_search(1)
    if b[0] != -1:
        print(real_time() + 'Нашел', b[1])
        x, y = b[0]
        rx = random.randint(-5, 5)
        ry = random.randint(-10, 10)
        api.core(x + rx, y + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(2)
        i = 0
        while i <= 5:
            time.sleep(1)
            storage_img = ['deposit_all.png']
            b = api.imgsearch(folder, storage_img, res, winname, 0).img_search(g_dev)
            i = i + 1
            if b[1] != -1:
                print(real_time() + 'Всё в банк', b[1])
                x, y = b[0]
                rx = random.randint(-5, 5)
                ry = random.randint(-10, 10)
                api.core(x + rx, y + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
                time.sleep(1)
                break
            else:
                print('Не нашел кнопки Депозита')
        d = 0
        while d <= 5:
            time.sleep(1)
            storage_img = ['bank_exit.png']
            b = api.imgsearch(folder, storage_img, res, winname, 0).img_search(g_dev)
            d += 1
            if b[1] != -1:
                print(real_time() + 'Закрываю банк', b[1])
                x, y = b[0]
                rx = random.randint(-5, 5)
                ry = random.randint(-10, 10)
                api.core(x + rx, y + ry, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
                inv = 0
                orecheck = 0
                if typebot == 4:
                    player_pos = 3
                break
            else:
                player_pos = 2
                print('Не закрыл Банк')
        v = 0
        while v <= 5:
            time.sleep(1)
            sword = ['sword.png']
            b = api.imgsearch('./img/check/', sword, .93, winname, 0).img_search(g_dev)
            v += 1
            if b[1] != -1:
                print(real_time() + 'Вышел с банка', b[1])
                time.sleep(1)
                break
            else:
                player_pos = 2
                print('Не закрыл Банк')


def use_storage(folder, img, res):
    global inv, orecheck
    b = api.imgsearch(folder, img, res, winname, 0).img_search(0)
    if b[0] != -1:
        x, y = b[0]
        r = random.randint(-5, 5)
        api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
        time.sleep(5)
        point1_pic = ['deposit_all.png']
        b = api.imgsearch('./img/bank/', point1_pic, 0.92, winname, 0).img_search(g_dev)
        if b[0] != -1:
            x, y = b[0]
            print(real_time() + 'Нашел ', point1_pic)
            r = random.randint(-7, 7)
            api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
            time.sleep(2)
            api.core(x, y, winname).esc(0.4)
            i = 0
            while i <= 6:
                time.sleep(1)
                point1_pic = ['sword.png']
                b = api.imgsearch('./img/check/', point1_pic, 0.92, winname, 0).img_search(g_dev)
                i += 1
                if b[0] != -1:
                    print(real_time() + 'Вроде закрыл банк')
                    inv = 0
                    orecheck = 0
                    break
            point1_pic = ['bank_exit.png']
            b = api.imgsearch('./img/bank/', point1_pic, 0.8, winname, 0).img_search(g_dev)
            if b[0] != -1:
                x, y = b[0]
                print(real_time() + 'Нашел ', point1_pic)
                r = random.randint(-2, 2)
                api.core(x + r, y + r, winname).adb_tap(bswinname, 0, 0, 0, 'tap_swipe')
                time.sleep(5)
                inv = 0
                orecheck = 0
        else:
            tbank(-3, 13, .9)
            print(real_time() + 'Not open storage')
    else:
        r = random.randint(300, 500)
        api.core(600, 100, winname).adb_tap(bswinname, 0, r, 3, 'swipe')
        time.sleep(3)
        time.sleep(3)
        tbank(-3, 13, .9)
        print(real_time() + 'Not found img 2')


def main():
    global player_pos, camera, stop, inv
    print('Добро пожаловать // Скрипт 3.0')
    print('( Мульти бот )')
    ran = random.randint(bstimer2, bstimer3)
    print('Время сна после выключения примерно: ', ran, ' сек')
    rt = random.randint(3, 10)
    # time.sleep(rt)
    q = 0
    thread_timer = Thread(target=timer_check)
    thread_timer.start()
    timer_off()
    while True:
        try:
            time.sleep(.5)
            # print('player_pos: ', player_pos, 'camera: ', camera, 'Invent: ', inv, 'orecheck', orecheck, typebot)
            q += 1
            if q >= 9:
                game_check()
                q = 0
            if info >= timer:
                ran = random.randint(bstimer2, bstimer3)
                stop = True
                print('Надо закрыть бота')
                thread_timer.join()
                timer_off()
                time.sleep(2)
                api.core(0, 0, winname).kill_app(bswinname)
                time.sleep(ran)
                api.core(0, 0, winname).run_app(bswinname)
                stop = False
                thread_timer = Thread(target=timer_check)
                thread_timer.start()
            if in_game == 2:
                time.sleep(.7)
                if camera == 0 and player_pos == 0:
                    time.sleep(5)
                    camera_to_default()
                elif camera == 1:
                    if typebot == 0:
                        btn = ['craft_btn.png']
                        folder = './img/'
                        protean(folder, btn, 0.9)
                    if typebot == 1:
                        if inv == 0:
                            ore_mining(sf1_folder, sf1_ore, sf1_ore_res)
                        elif inv == 1:
                            sleep = 6
                            sf_storage(sf1_folder, sf1_storage, sleep, sf1_storage_res)
                    if typebot == 2:
                        if inv == 0:
                            ore_mining(sf2_folder, sf2_ore, sf2_ore_res)
                        elif inv == 1:
                            to_storage()
                            sleep = 4
                            sf_storage(sf2_folder, sf2_storage, sleep, sf2_storage_res)
                            to_mining()
                    if typebot == 3:
                        if inv == 0:
                            third_ore_mining(tiron_folder, tiron_ore, tiron_ore_res)
                        elif inv == 1:
                            print('Inventory FULL')
                            tbank(-3, 13, .9)

                            use_storage(tiron_storage_folder, tiron_storage, tiron_storage_res)

                            tbank(122, 0, .9)

                            thread_inv = Thread(target=ore_check_fast)
                            thread_inv.start()
                    if typebot == 4:
                        # print('working')
                        if player_pos == 0 and inv == 1:
                            #print('Телепорт')
                            teleport_book()
                        elif player_pos == 1:
                            #print('В банк')
                            tyrian_bank_point()
                        elif player_pos == 2:
                            new_storage(tyrian_storage_folder, tyrian_storage, tyrian_storage_res)
                        elif player_pos == 3:
                            tbank(57, -12, .9, 15, 16)
                            enter_dang()
                        elif player_pos == 4:
                            tmining_point()
                        elif player_pos == 5:
                            ore_mining(tyrian_folder, tyrian_ore, tyrian_ore_res)

                                # thread_inv = Thread(target=ore_check_fast)
                                # thread_inv.start()
        except Exception:
            print(real_time() + 'Исключение сработало, цыкл нарушен')
            continue

if __name__ == '__main__':
    main()