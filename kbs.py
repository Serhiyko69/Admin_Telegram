from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Створити зустріч')
b2 = KeyboardButton('Переглянути активні зустрічі')

kb_client.add(b1).add(b2)

#############################################################################
cities = {
'Львівська':[
'Львів',
'Золочів',
'Броди',
'Стрий',
'Буськ',
'Яворів',
'Городок',
'Самбір'],

'Київська': [
'Київ',
'Ірпінь',
'Біла Церква',
'Бровари',
'Обухів',
'Бородянка',
'Фастів',
'Бориспіль'],

'Харківська': [
'Харків',
'Ізюм'],

'Одеська': [
'Одеса',
'Ізмаїл']
}

location_k = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

for region, city_list in cities.items():
    region_button = KeyboardButton(region)
    location_k.add(region_button)
#############################################################################
kb_region = ReplyKeyboardMarkup(resize_keyboard=True)

b3 = KeyboardButton({'Львівська': ['Львів', 'Дрогобич']})
b4 = KeyboardButton('Київська')
b5 = KeyboardButton('Харківська')
b6 = KeyboardButton('Одеська')

kb_region.add(b3).add(b4).add(b5).add(b6)
#############################################################################

kb_Lviv = ReplyKeyboardMarkup(resize_keyboard=True)

Lviv1 = KeyboardButton('Львів')
Lviv2 = KeyboardButton('Золочів')
Lviv3 = KeyboardButton('Броди')
Lviv4 = KeyboardButton('Стрий')
Lviv5 = KeyboardButton('Буськ')
Lviv6 = KeyboardButton('Яворів')
Lviv7 = KeyboardButton('Городок')
Lviv8 = KeyboardButton('Самбір')

kb_Lviv.add(Lviv1).add(Lviv2).add(Lviv3).add(Lviv4).add(Lviv5).add(Lviv6).add(Lviv7).add(Lviv8)
#############################################################################

kb_Kyiv = ReplyKeyboardMarkup(resize_keyboard=True)

Kyiv1 = KeyboardButton('Київ')
Kyiv2 = KeyboardButton('Ірпінь')
Kyiv3 = KeyboardButton('Біла Церква')
Kyiv4 = KeyboardButton('Бровари')
Kyiv5 = KeyboardButton('Обухів')
Kyiv6 = KeyboardButton('Бородянка')
Kyiv7 = KeyboardButton('Фастів')
Kyiv8 = KeyboardButton('Бориспіль')

kb_Kyiv.add(Kyiv1).add(Kyiv2).add(Kyiv3).add(Kyiv4).add(Kyiv5).add(Kyiv6).add(Kyiv7).add(Kyiv8)
#############################################################################

keyboard = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(text="Вказати дату і час", callback_data="set_datetime")
keyboard.insert(button)

kb_cancel = kb_Kyiv = ReplyKeyboardMarkup(resize_keyboard=True)
cancel = KeyboardButton('Відмінити')
kb_cancel.add(cancel)



year_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
for year in range(2023, 2030):  # Змініть діапазон на потрібний
    year_button = KeyboardButton(str(year))
    year_keyboard.add(year_button)


# Створення клавіатури для вибору місяця
month_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
for month in range(1, 13):
    month_button = KeyboardButton(str(month))
    month_keyboard.add(month_button)

# Створення клавіатури для вибору дня
day_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
for day in range(1, 32):
    day_button = KeyboardButton(str(day))
    day_keyboard.add(day_button)

# Створення клавіатури для вибору години
hour_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
for hour in range(0, 24):
    hour_button = KeyboardButton(str(hour))
    hour_keyboard.add(hour_button)

# Створення клавіатури для вибору хвилини
minute_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
for minute in range(0, 60, 5):  # Змініть крок на потрібний
    minute_button = KeyboardButton(str(minute))
    minute_keyboard.add(minute_button)



