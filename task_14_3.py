from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

path_to_key = __file__.rsplit('/', maxsplit=3)[0]
with open(f'{path_to_key}/Документы/aiogram_api_key', 'r') as key:
    api = key.read().splitlines()
bot = Bot(token=api[0])
dp = Dispatcher(bot=bot, storage=MemoryStorage())

classic_kb = ReplyKeyboardMarkup(resize_keyboard=True)
classic_button_1 = KeyboardButton(text='Расчитать')
classic_button_2 = KeyboardButton(text='Информация')
classic_button_3 = KeyboardButton(text='Купить')
classic_kb.add(classic_button_1)
classic_kb.add(classic_button_2)
classic_kb.add(classic_button_3)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_button_1, inline_button_2)

inline_buy_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_buy_button_1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
inline_buy_button_2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
inline_buy_button_3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
inline_buy_button_4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
inline_buy_kb.row(inline_buy_button_1, inline_buy_button_2, inline_buy_button_3, inline_buy_button_4)


tabs_names = ('Помагин', 'Неболин', 'Работин', 'Соннеслабин')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет!', reply_markup=classic_kb)


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я бот помогающий твоему здоровью.'
                         'Если хотите узнать Вашу суточную норму калорий, нажмите кнопку "Расчитать"')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'img/{i}.webp', 'rb') as image:
            await message.answer_photo(image,
                                 f'Название: {tabs_names[i-1]}\nОписание: описание {i}\nЦена: {i * 100}')
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_buy_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {result}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
