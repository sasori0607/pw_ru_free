import time
import keyboard


#сервер 1 = камбекб, сервер 2 = Ультра нью
server = 1


class Goods:
    def __init__(self, name, anchor, condition=0, kof=0):
        self.name = name
        self.anchor = anchor
        self.condition = condition
        self.kof = kof



    def clicks(self):
        print('start clicks')
        if self.condition == 0:
            keyboard.press_and_release('enter')
            time.sleep(0.5)
            keyboard.press_and_release('enter')
            time.sleep(1)
        elif self.condition == 1:
            keyboard.press_and_release('enter')
            time.sleep(0.5)
            keyboard.press_and_release('up')
            time.sleep(0.5)
            keyboard.press_and_release('enter')
            time.sleep(1)

#Cambek
if server == 1:

    perfect_prize = Goods('Идеальный приз', 'perfect_prize', 0, -1)

    stone_of_immortals = Goods('Камень бессмертных', 'stone_of_immortals', 1, -1)

    treasure_of_the_past = Goods('Сокровище прошлого', 'treasure_of_the_past', 0, -1)

    wonderful_crystal = Goods('Чудесный кристалл', 'wonderful_crystal')

    knife_emblem = Goods('Эмблема ножа', 'knife_emblem', 0, -1)

    moon_crystal = Goods('Лунный кристалл', 'moon_crystal')

    collectible_coin = Goods('Коллекционная монета', 'collectible_coin', 0, -1)

    shield_medal = Goods('Медаль в виде щита', 'shield_medal', 0, -1)




#Ultra New
if server == 2:

    perfect_prize = Goods('Идеальный приз', 'perfect_prize', 0, -1)

    stone_of_immortals = Goods('Камень бессмертных', 'stone_of_immortals', 1, -1)

    witch_knot = Goods('Узелок ведьмы', 'witch_knot', 0, 0)

    moon_steel = Goods('Лунная сталь', 'moon_steel', 0, -1)

    bronze_coin = Goods('Бронзовая монета', 'bronze_coin')

    knife_emblem = Goods('Эмблема ножа', 'knife_emblem', 0, -1)

    collectible_coin = Goods('Коллекционная монета', 'collectible_coin', 0, -1)

    shield_medal = Goods('Медаль в виде щита', 'shield_medal', 0, 1)

    xuan_yuan_stone = Goods('Камень Сюань Юань', 'xuan_yuan_stone', 0, -1)



my_budget_26_08_21 = '30чеков, старт в конце дня 22:04 КАМБЕК'



