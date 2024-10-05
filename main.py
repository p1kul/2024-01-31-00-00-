from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = '7735380637:AAHpdvn8A9aM7zctdMPntzEHaUfJoATj5wY'
bot = Bot(api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button1,button2,button3)
kb.resize_keyboard

keybord = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
keybord.add(but1,but2)

keybord_for_buy = InlineKeyboardMarkup()
but3 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
but4 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
but5 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
but6 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
keybord_for_buy.add(but3, but4, but5, but6)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=keybord)

@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    with open('6026051787.jpg','rb') as img:
        await message.answer_photo(img,f'Название: Product1 | Описание: описание 1 | Цена: 100 ')
    with open('c60bda359ec2c99b70a726718e5cb08a.png','rb') as img:
        await message.answer_photo(img,f'Название: Product2 | Описание: описание 2 | Цена: 200 ')
    with open('cee0f548474657dffc6263b36e635471.jpg', 'rb') as img:
        await message.answer_photo(img,f'Название: Product3 | Описание: описание 3 | Цена: 300 ')
    with open('maxler-creatine-500-gr-arbuz_-mcp.jpg', 'rb') as img:
        await message.answer_photo(img,f'Название: Product4 | Описание: описание 4 | Цена: 400 ')
    await message.answer('Выберите продукт для покупки: ', reply_markup=keybord_for_buy)
    
@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(возраст=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def  set_weight(message, state):
    await state.update_data(рост=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(вес=message.text)
    data = await state.get_data()
    calories = 10*int(data['возраст'])+6.25*int(data['рост'])-5*int(data['вес'])+5
    await message.answer(f"Ваша норма калорий {calories}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
