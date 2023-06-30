from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from func import Consts, conf_bot
from aiogram.dispatcher.filters import Text

from config import bot_token
consts = Consts()

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    your_name = State()
    partner_name = State()


@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals='start', ignore_case=True), state='*')
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="help")],
        [types.KeyboardButton(text="try")],
        [types.KeyboardButton(text="cancel")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Привет! Я ебанутая хуйня.\n'
                         'Я умею считать вашу совместимость по именам.\n'
                         'Кринж ебаный? Я тоже так думаю.\n\n'
                         'Чтобы начать, нажмите или напишите try.', reply_markup=keyboard)


@dp.message_handler(commands=['help'])
@dp.message_handler(Text(equals='help', ignore_case=True), state='*')
async def send_help(message: types.Message):
    kb = [
        [types.KeyboardButton(text="try")],
        [types.KeyboardButton(text="cancel")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Чтобы начать, нажмите или напишите try.\n'
                         'А что говорить, блять? Ну, хуй.', reply_markup=keyboard)


@dp.message_handler(commands=['try'])
@dp.message_handler(Text(equals='try', ignore_case=True), state='*')
async def get_your_name(message: types.Message):
    kb = [
        [types.KeyboardButton(text="cancel")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await Form.your_name.set()
    await message.answer('Как вас зовут?', reply_markup=keyboard)


@dp.message_handler(state=Form.your_name)
async def process_your_name(message: types.Message, state: FSMContext):
    if message.text != 'cancel':
        async with state.proxy() as data:
            data['your_name'] = message.text
        consts.set_your_name(message.text)
    else:
        await cancel_handler(message, state)
        return

    kb = [
        [types.KeyboardButton(text="cancel")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await Form.next()
    await message.answer('Как зовут вашего партнёра?', reply_markup=keyboard)


@dp.message_handler(state=Form.partner_name)
async def process_partner_name(message: types.Message, state: FSMContext):
    if message.text != 'cancel':
        async with state.proxy() as data:
            data['partner_name'] = message.text
        consts.set_partner_name(message.text)
    else:
        await cancel_handler(message, state)
        return

    kb = [
        [types.KeyboardButton(text="finish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await Form.next()
    await message.answer(f'Ваша совместимость - {conf_bot(consts.name1, consts.name2)}%.\n'
                         f'Чтобы выйти, нажмите или напишите finish.',
                         reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state='*', commands=['cancel', 'finish'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
@dp.message_handler(Text(equals='finish', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):

    await message.answer('Ты слит.\nЧтобы начать заново, нажмите или напишите start.',
                         reply_markup=types.ReplyKeyboardRemove())
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()


def start_bot():
    executor.start_polling(dp, skip_updates=True)
