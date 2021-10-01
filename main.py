from mouse_control_functions import *
from my_objects import *
import time
from functions import *
import keyboard
import json
import datetime
from telegram import mess_error, mess_start



if __name__ == "__main__":

    mess_start()
    counter = 0
    if server == 1:
        all_list = [stone_of_immortals, treasure_of_the_past, perfect_prize, collectible_coin, shield_medal, knife_emblem, moon_crystal,
                    wonderful_crystal
                    ]
    elif server == 2:
        all_list = [stone_of_immortals, collectible_coin, perfect_prize, witch_knot,
                    shield_medal, moon_steel,
                    knife_emblem]
    while True:
        for i in range(len(all_list)):
            try:
                all_info_json = open_json(server)
                entry_into_products(all_list[i])
                _, min_price_sales = collection_of_all_prices(all_list[i].kof)
                x,y = search_on_screen_2('tmp/change_of_purchase_section.bmp')
                mouse_move(x, y)
                mouse_click()
                max_purchases, _ = collection_of_all_prices(all_list[i].kof)
                print('Минимальная цена продажи = ', min_price_sales)
                print('Максимальная цена закупки = ', max_purchases)

                all_menu_exit()
                entry_into_my_lots()
                var1, var2 = storage(all_info_json[all_list[i].anchor])
                all_menu_exit()
                if var1 != 0:
                    key, new_min_price_sales, new_max_purchases = check_price_change(min_price_sales, max_purchases,
                                                                                     all_info_json[all_list[i].anchor],
                                                                                     all_list[i].anchor)
                    key += 1
                else:
                    key, new_min_price_sales, new_max_purchases = check_price_change(min_price_sales, max_purchases,
                                                                                     all_info_json[all_list[i].anchor],
                                                                                     all_list[i].anchor)
                all_info_json = open_json(server)
                print('key = ', key, '###############################')
                if key > 0:
                    entry_into_my_lots()
                    clear_commission(all_info_json[all_list[i].anchor])
                    var1, var2 = storage(all_info_json[all_list[i].anchor])
                    if var1 != 0 and var2 != 0:
                        mouse_move_click(var1, var2)
                    all_menu_exit()
                    entry_into_my_lots()
                    installation_goods(all_info_json[all_list[i].anchor], server)
                    all_menu_exit()
                counter = 0
            except:

                x = scan_disconnect()
                counter += x
                all_menu_exit()
                x, y = search_on_screen_2('tmp/cancellation.bmp', **{'key': '1'})
                if x != 0 and y != 0:
                    mouse_move_click(x, y)
                    time.sleep(2)
                all_menu_exit()

                # if counter >= 20:
                #
                #     f = open('logs.txt', 'a')
                #     mess_error()
                #     f.write(str(datetime.datetime.now()) + str(counter) + '\n')
                #     time.sleep(1)
                #     os.system("shutdown -t 0 -r -f")

                if counter % 5 == 0:
                    print('kill')
                    os.system("taskkill /f /im elementclient.exe")
                    os.startfile("exe")
                    time.sleep(90)
                    if server == 1 or server == 2:
                        x, y = search_on_screen_2('tmp/icon.bmp')
                        mouse_move_click(x, y)
                        time.sleep(5)
                    for i in range(4):
                        keyboard.press_and_release('esc')
                        time.sleep(12)
                    time.sleep(150)














