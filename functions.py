import time
import pytesseract
import cv2
import numpy
import pyperclip
from mouse_control_functions import *
from my_objects import *
import json


def scan_prices(img):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    #первый вариант конвертирование изображение в чб вариант для тесракта(рабочий)
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.divide(image, 450, scale=455)

    # второй вариант конвертирование изображение в чб вариант для тесракта(рабочий)

    # image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    # thresh = 55 #64 #55
    # image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]


    cv2.imwrite('res2.png', image)




    # получаем строку
    #string = pytesseract.image_to_string(image, lang='rus', config=' --psm 12') #для текста
    string = pytesseract.image_to_string(image, config=' --psm 6 --oem 3 -c tessedit_char_whitelist=0123456789,')
    return string


def search_on_screen(img, *cords):

    method = cv2.TM_SQDIFF_NORMED

    small_image = cv2.imread(img)
    small_image = cv2.cvtColor(small_image, cv2.COLOR_RGB2GRAY)

    if cords:
        print('region', cords[0], cords[1], cords[2], cords[3])
        screen = pyautogui.screenshot(region=(cords[0], cords[1], cords[2], cords[3]))
    else:
        screen = pyautogui.screenshot()
    screen = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(small_image, screen, method)
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    MPx, MPy = mnLoc
    trows, tcols = small_image.shape[:2]
    h = (MPx + tcols // 2)
    v = (MPy + trows // 2)
    print(h, v)

    if cords:
        h = h + cords[0]
        v = v + cords[1]


    return h, v


def search_on_screen_2(img_discov, *cords, **kwargs):

    start_time = time.time()
    x = 0
    src_rgb = cv2.imread(img_discov)
    src_gray = cv2.cvtColor(src_rgb, cv2.COLOR_BGR2GRAY)

    while x==0:
        if cords:
            print('region', cords[0],cords[1],cords[2],cords[3])
            screen = pyautogui.screenshot(region=(cords[0],cords[1],cords[2],cords[3]))
        else:
            screen = pyautogui.screenshot()
        screen = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2GRAY)
        #коорды
        w, h = src_gray.shape[::-1]
        res = cv2.matchTemplate(screen, src_gray, cv2.TM_CCOEFF_NORMED)

        threshold = 0.87

        loc = numpy.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (250,0,255), 1)
            print("++")
            cv2.imwrite('res.png',screen)
            x=2
            #получаемые знач
            print((loc[1][0]), (loc[0][0]), w, h)
            if cords:
                x = (loc[1][0]) + cords[0]
                y = (loc[0][0]) + cords[1]
            else:
                x = (loc[1][0])
                y = (loc[0][0])
            return x, y
        else:
            print("-", time.time() - start_time)
            cv2.imwrite('res_error.png', screen)
            if 'key' in kwargs:
                if kwargs['key'] == '1':
                    return 0, 0
            if time.time() - start_time > 15:
                return "error"


def search_on_screen_2_all_obj(img_discov, *cords):
    k = 0
    x1, y1, v1, h1 = cords
    y2 = 0
    key = {"key": "1"}
    while True:
        print(x1, y1+y2, v1, h1, 'search_on_screen_2_all_obj')
        x, y = search_on_screen_2(img_discov, x1, y1+y2, v1, h1, **key)
        if x != 0 and y != 0:
            k += 1
            y2 = y - y1 + 5
            print(y2, 'y2')
            print(k, 'K')
        else:
            return k


def collection_of_all_prices(k=0):

    x_start, y_start = search_on_screen_2('tmp/coin.bmp')
    min_price = None
    first_list = []
    second_list = []
    x, y = x_start, y_start
    print('start scan price')
    while True:
        for i in range(20):
            # default = pyautogui.screenshot(region=(x - 100, y - 4, 97, 18))
            if server == 1:
                screen = pyautogui.screenshot(region=(x - 100, y - 3, 97, 18-k))
            elif server == 2:
                screen = pyautogui.screenshot(region=(x - 100, y - 3, 97, 18 - k))


            screen = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2GRAY)
            cv2.imwrite('res.png', screen)
            el = scan_prices('res.png')[0:-2].split('\n')[0]
            el_split = el.split(',')
            el = ''.join(el_split)
            if el != '':
                el = int(el)
                second_list.append(el)

            if i % 2 == 1:
                y += 36
                if i > 0:
                    x -= 254
            else:
                x += 254
        #second_list = filter(None, second_list)
        print(second_list,'list prices')
        page_max = max(second_list)
        page_min = min(second_list)
        if 'general_max' in locals():
            if general_max < page_max:
                general_max = page_max
            if general_min > page_min:
                general_min = page_min
        else:
            general_max = page_max
            general_min = page_min

        if first_list == second_list:
            return general_max, general_min
        else:
            cord1, cord2 = search_on_screen_2('tmp/btn_next_page.bmp')
            mouse_move(cord1, cord2)
            mouse_click()
            time.sleep(0.4)
            first_list = second_list
            second_list = []
            x, y = x_start, y_start



    #110 20
    # screen = pyautogui.screenshot(region=(x-100, y-3, 95, 20))
    # screen = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2GRAY)
    # cv2.imwrite('res.png', screen)
    # scan_prices('res.png')


def check_cords_and_dbl_cl(x, y):

    if x != 0 and y != 0:
        mouse_move(x, y)
        for i in range(3):
            mouse_click()
            time.sleep(0.1)


def clear_commission(data):
    print(data['ref'])
    x_1, y_1 = search_on_screen_2('tmp/inscription_sel.bmp')
    x_2, y_2 = search_on_screen_2('tmp/inscription_buy.bmp')
    key = {"key": "1"}
    x, y = search_on_screen_2(data['ref'], x_1-5, y_1, x_2-x_1, 185, **key)
    check_cords_and_dbl_cl(x, y)

    x, y = search_on_screen_2(data['ref'], x_2 - 9, y_2, x_2 - x_1, 190, **key)
    check_cords_and_dbl_cl(x, y)


def all_menu_exit():
    x, y = search_on_screen_2('tmp/exit.bmp', **{'key': '1'})
    if x != 0 and y != 0:
        mouse_move_click(x,y)
        time.sleep(0.2)
    for i in range(7):
        keyboard.press_and_release('esc')
        time.sleep(0.2)



def entry_into_products(object):

    #дополнительный выход с меню нипа
    all_menu_exit()

    # поиск нипа
    x, y = search_on_screen_2('tmp/nps.bmp')
    mouse_move(x + 2, y + 2)
    mouse_click()

    # убираем рандом, скидывае подсветку поля на кнопку назад
    x, y = search_on_screen_2('tmp/btn_back.bmp')
    mouse_move(x + 1, y + 2)

    # переходим в общий раздел комки
    x, y = search_on_screen_2('tmp/commission_shop_chapter.bmp')
    mouse_move(x + 1, y + 2)
    mouse_click()

    # находим кнопку поиска, и переходим на поиск
    x, y = search_on_screen_2('tmp/templ_btn_s.bmp')
    mouse_move(x - 25, y - 2)
    mouse_click()
    time.sleep(0.2)
    pyperclip.copy(object.name)
    keyboard.press_and_release('ctrl + v')
    time.sleep(1)
    object.clicks()


def entry_into_my_lots():

    all_menu_exit()
    # поиск нипа
    x, y = search_on_screen_2('tmp/nps.bmp')
    mouse_move(x + 2, y + 2)
    mouse_click()

    # убираем рандом, скидывае подсветку поля на кнопку назад
    x, y = search_on_screen_2('tmp/btn_back.bmp')
    mouse_move(x + 1, y + 2)

    # переходим в наши лоты
    x, y = search_on_screen_2('tmp/Thrift_store_section_with_my_lots.bmp')
    mouse_move(x + 1, y + 2)
    mouse_click()


def storage(data):
    x, y = search_on_screen_2('tmp/btn_storage.bmp')
    mouse_move_click(x,y)
    time.sleep(0.1)
    x, y = search_on_screen_2('tmp/word_subjects.bmp')
    key = {"key": "1"}
    x, y = search_on_screen_2(data['ref'], x - 10, y, 300, 150, **key)
    return x, y


def clean_field():
    for i in range(9):
        keyboard.press_and_release('backspace')
        time.sleep(0.1)


def check_price_change(min_price_sales, max_purchases, data, obj):

    key = 0
    print(int(min_price_sales) - int(max_purchases), int(data['min_profit']), '##############################')
    if int(min_price_sales) - int(max_purchases) >= int(data['min_profit']):
        if int(min_price_sales) != int(data['last_sale_price']):
            price_sales = int(min_price_sales) - int(data['step'])
            print(price_sales)
            all_info_json = open_json(server)
            all_info_json[obj]['last_sale_price'] = price_sales
            write_json(server, all_info_json)
            key += 1
        else:
            price_sales = data['last_sale_price']
        if int(max_purchases) != int(data['last_price_of_my_purchase']):
            price_purchases = max_purchases + int(data['step'])
            all_info_json = open_json(server)
            all_info_json[obj]['last_price_of_my_purchase'] = price_purchases
            write_json(server, all_info_json)
            key += 1
        else:
            price_purchases = data['last_price_of_my_purchase']
        return key, price_sales, price_purchases
    else:
        #ключ ошибки цен
        return -5, 0, 0


def installation_goods(data, server):

    number_sales = 0
    x_1, y_1 = search_on_screen_2('tmp/inscription_sel.bmp')
    x_2, y_2 = search_on_screen_2('tmp/inscription_buy.bmp')
    k = search_on_screen_2_all_obj(data['ref'], x_2+(x_2-x_1), y_2, 1280, 800)
    if k > 1:
        x, y = search_on_screen_2(data['ref'], x_2+(x_2-x_1), y_2, 1280, 800)
        mouse_move(x, y)
        mouse_click_and_move(x_1+(x_2-x_1)/2, y_1+100)
        x, y = search_on_screen_2('tmp/max.bmp')
        mouse_move_click(x, y)
        screen = pyautogui.screenshot(region=(x-76, y-6, 40, 18))
        screen = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2GRAY)
        cv2.imwrite('res.png', screen)
        el = scan_prices('res.png')[0:-2].split('\n')[0]
        el_split = el.split(',')
        number_sales = ''.join(el_split)
        x, y = search_on_screen_2('tmp/price.bmp')
        mouse_move_click(x+100, y+5)
        pyperclip.copy(data['last_sale_price'])
        clean_field()
        keyboard.press_and_release('ctrl + v')
        mouse_move_click(x + 45, y + 59)
        time.sleep(1)
    if k >= 1:
        price_purchases = int(data['last_price_of_my_purchase'])
        amount_purchases = round((int(data['budget']) - (int(data['last_sale_price']) * int(number_sales))) / price_purchases)
        if amount_purchases > 0:
            time.sleep(0.3)
            x, y = search_on_screen_2(data['ref'], x_2 + (x_2 - x_1), y_2, 1280, 800)
            mouse_move(x, y)
            time.sleep(0.2)
            mouse_click_and_move(x_2 + (x_2 - x_1) / 2, y_2 + 100)
            time.sleep(0.3)

    #old v с зависанием
    #     x, y = search_on_screen_2('tmp/amount.bmp')
    #     mouse_move_click(x+90, y+7)
    #     price_purchases = int(data['last_price_of_my_purchase'])
    #     amount_purchases = round((int(data['budget']) - (int(data['last_sale_price']) * int(number_sales))) / price_purchases)
    #     pyperclip.copy(amount_purchases)
    #     clean_field()
    #     keyboard.press_and_release('ctrl + v')
    #     time.sleep(0.3)
    #     x, y = search_on_screen_2('tmp/price.bmp')
    #     mouse_move_click(x + 100, y + 5)
    #     pyperclip.copy(price_purchases)
    #     clean_field()
    #     keyboard.press_and_release('ctrl + v')
    #     time.sleep(0.1)
    #     mouse_move_click(x + 45, y + 59)
    #     time.sleep(0.3)

            pyperclip.copy(price_purchases)
            clean_field()
            time.sleep(0.1)
            keyboard.press_and_release('ctrl + v')
            time.sleep(0.3)
            keyboard.press_and_release('tab')
            time.sleep(0.3)
            pyperclip.copy(amount_purchases)
            clean_field()
            keyboard.press_and_release('ctrl + v')
            time.sleep(0.3)
            keyboard.press_and_release('enter')
            time.sleep(1)
            key = {'key': '1'}
            if server == 1:
                x, y = search_on_screen_2('tmp/accept.bmp', **key)
            elif server == 2:
                x, y = search_on_screen_2('tmp/accept_ultanew.bmp', **key)
            if x != 0 and y != 0:
                mouse_move_click(x, y)


def scan_disconnect():
    key = {'key': '1' }
    x, y = search_on_screen_2('tmp/disconent.bmp', **key)
    if x != 0 and y != 0:
        #перезаход
        return 1000
    else:
        return 1


def open_json(server):

    if server == 1:
        with open('data_file_comeback.json', encoding='utf-8') as f:
            all_info_json = json.load(f)
    elif server == 2:
        with open('data_file_new.json', encoding='utf-8') as f:
            all_info_json = json.load(f)

    return all_info_json


def write_json(server, data):
    if server == 1:
        with open('data_file_comeback.json', 'w') as f:
            json.dump(data, f)
    elif server == 2:
        with open('data_file_new.json', 'w') as f:
            json.dump(data, f)
















