import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from states_machine import ReceiptStates
from parser_receipt import get_html_doc, find_link_and_name, parse_receipt
from config import TOKEN_BOT


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Принимает команду пользователя (старт или хелп)
     и отправляет сообщение-приветствие
    :param message: команда пользователя start или help
    """
    await message.reply('Привет!\nЯ рецепт-бот!')
    await message.answer('Чтобы получить случайный рецепт введи команду /receipt' +
                         '\nБот отправит тебе название рецепта. Если хочешь получить полный рецепт - вводи команду /да')


@dp.message_handler(commands=['receipt'], state='*')
async def random_receipt_name(message: types.Message, state: FSMContext):
    """
    Принимает сообщение пользователя и отвечает сообщением с именем рецепта
    :param message: входящее сообщение от пользователя
           state: текущее состояние машины состояний
    """
    await ReceiptStates.confirm.set()

    html_doc = await get_html_doc('https://www.gotovim.ru/sbs/random.shtml')
    await message.answer(find_link_and_name(html_doc)[0])

    async with state.proxy() as data:
        data['name'] = find_link_and_name(html_doc)[0]
        data['link'] = find_link_and_name(html_doc)[1]


@dp.message_handler(commands=['да', 'Да', 'ДА', 'confirm'], state=ReceiptStates.confirm)
async def get_full_receipt(message: types.Message, state: FSMContext):
    """
    Отправляет несколько сообщений от бота с полным рецептом блюда
    :param message: сообщение от пользователя с текстом 'да'

    """
    async with state.proxy() as data:
        html_doc = await get_html_doc(data['link'])
        receipt = parse_receipt(html_doc)

        await message.reply('Рецепт ' + receipt['name'])
        await message.answer('Ингридиенты\n' + '\n'.join(receipt['ingridients']))

        for index, step in enumerate(receipt['receipt_text']):
            await message.answer(f'{str(index + 1)}) {step}')

        await message.answer(data['link'])

        await state.finish()


@dp.message_handler(state=ReceiptStates.confirm)
async def cancel_receipt(message: types.Message, state: FSMContext):
    """
    Отправляет пользователю сообщение с указанием на ввод нужной команды.

    :param message: сообщение пользователя
    :param state: состояние машины состоянии равное confirm

    """

    await message.answer('Если хотите получить следующий рецепт, введите команду /receipt')
    await state.finish()


@dp.message_handler()
async def echo(message: types.Message):
    """

    :param message:
    :return:
    """

    await message.reply('Пожалуйста, отправьте боту команду /start или /help для получения инструкций по работе с ботом.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
