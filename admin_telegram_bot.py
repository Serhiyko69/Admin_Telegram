import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from kbs import *
from connect import TOKEN, collection


storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

#ID вашої групи
GROUP_ID = -970835123



@dp.message_handler(commands=['start'])
async def start_def(message: types.Message):
    await message.answer('Привіт, що хочеш зробити?', reply_markup=kb_client)


@dp.message_handler(text=['Створити зустріч'])
async def start_def(message: types.Message):
    await message.answer('Обери свою область та місто', reply_markup=location_k)


@dp.message_handler(text=list(cities.keys()))  # Обробляємо натискання на кнопки областей
async def cmd_choose_region(message: types.Message, state: FSMContext):
    selected_region = message.text

    # Створюємо клавіатуру для міст обраної області
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for city in cities[selected_region]:
        city_button = KeyboardButton(city)
        keyboard.add(city_button)

    await message.answer(f'Ви обрали область: {selected_region}. Виберіть місто:', reply_markup=keyboard)

    # Зберігаємо обрану область у стані
    async with state.proxy() as data:
        data['selected_region'] = selected_region


# Обробник натискання на кнопки міст
@dp.message_handler(lambda message: message.text in [city for cities_list in cities.values() for city in cities_list])
async def cmd_choose_city(message: types.Message, state: FSMContext):
    selected_city = message.text

    async with state.proxy() as data:
        selected_region = data['selected_region']

    await message.answer(f'Ви обрали {selected_region} область, місто: {selected_city} ')

    # Зберігаємо обране місто у стані
    async with state.proxy() as data:
        data['selected_city'] = selected_city

    # Додаємо клавіатуру з роками
    await message.answer('Виберіть рік:', reply_markup=year_keyboard)
    await state.set_state('waiting_for_year')  # Встановлюємо стан для очікування року


# Обробник вибору року
@dp.message_handler(lambda message: message.text.isdigit(), state='waiting_for_year')
async def process_year_input(message: types.Message, state: FSMContext):
    selected_year = int(message.text)
    await message.answer('Виберіть місяць:', reply_markup=month_keyboard)
    await state.update_data(year=selected_year)  # Зберігаємо обраний рік у стані
    await state.set_state('waiting_for_month')  # Встановлюємо стан для очікування місяця


# Обробник вибору місяця
@dp.message_handler(lambda message: message.text.isdigit(), state='waiting_for_month')
async def process_month_input(message: types.Message, state: FSMContext):
    selected_month = int(message.text)
    await message.answer('Виберіть день:', reply_markup=day_keyboard)
    await state.update_data(month=selected_month)  # Зберігаємо обраний місяць у стані
    await state.set_state('waiting_for_day')  # Встановлюємо стан для очікування дня


# Обробник вибору дня
@dp.message_handler(lambda message: message.text.isdigit(), state='waiting_for_day')
async def process_day_input(message: types.Message, state: FSMContext):
    selected_day = int(message.text)
    await message.answer('Виберіть годину:', reply_markup=hour_keyboard)
    await state.update_data(day=selected_day)  # Зберігаємо обраний день у стані
    await state.set_state('waiting_for_hour')  # Встановлюємо стан для очікування години


# Обробник вибору години
@dp.message_handler(lambda message: message.text.isdigit(), state='waiting_for_hour')
async def process_hour_input(message: types.Message, state: FSMContext):
    selected_hour = int(message.text)
    await message.answer('Виберіть хвилину:', reply_markup=minute_keyboard)
    await state.update_data(hour=selected_hour)  # Зберігаємо обрану годину у стані
    await state.set_state('waiting_for_minute')  # Встановлюємо стан для очікування хвилини


# Обробник вибору хвилини
@dp.message_handler(lambda message: message.text.isdigit(), state='waiting_for_minute')
async def process_minute_input(message: types.Message, state: FSMContext):
    selected_minute = int(message.text)

    async with state.proxy() as data:
        user_id = message.from_user.id
        selected_region = data["selected_region"]
        selected_city = data["selected_city"]
        selected_year = data["year"]
        selected_month = data["month"]
        selected_day = data["day"]
        selected_hour = data["hour"]

    # Збереження інформації про дату та час
    date_time = datetime.datetime(selected_year, selected_month, selected_day, selected_hour, selected_minute)
    formatted_date_time = date_time.strftime('%Y-%m-%d %H:%M')

    # Збереження всієї інформації в базу даних
    user_data = {
        "user_id": user_id,
        "region": selected_region,
        "city": selected_city,
        "datetime": formatted_date_time,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(user_data)

    # Вивід інформації про зустріч
    response = (
        f"Ваша зустріч відбудеться у місті {selected_city}, {selected_region} область, "
        f"Дата: {formatted_date_time}"
    )
    await message.answer(response)

    # Створення кнопки для додавання ідентифікатора користувача в базу даних
    join_button = types.InlineKeyboardButton("Приєднатися", callback_data=user_id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(join_button)

    # Опублікувати повідомлення у групі з кнопкою
    post_message = f"Нова зустріч: {formatted_date_time} у {selected_city}, {selected_region} область"
    await bot.send_message(GROUP_ID, post_message, reply_markup=keyboard)

    await state.finish()


# Обробник натискання на кнопку "Приєднатися"
@dp.callback_query_handler(lambda callback_query: True)
async def join_meeting(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id

    # Додати код для збереження user_id в базу даних тут
    doc = {
        "add_user": user_id
    }
    collection.insert_one(doc)
    await bot.answer_callback_query(callback_query.id, text="Ви приєднались до зустрічі!")


# Решта коду незмінна

# Функція-запуск при старті
async def on_startup(_):
    print('Бот запущено')


# Запуск бота
if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup)