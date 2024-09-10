from aiogram import Router, F,  html
import asyncio
from bs4 import BeautifulSoup as bs
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
import requests
from data_base import site_url, site_headers
from keyboards import pre_start_clava
from aiogram.enums import ParseMode
from filters import PRE_START, IS_LETTER
from lexicon import *
from postgres_functions import *


ch_router = Router()

@ch_router.message(~F.text)
async def delete_not_text_type_messages(message: Message):
    await message.delete()


@ch_router.message(CommandStart())
async def process_start_command(message: Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    data = await check_user_in_table(user_id)
    if not data:
        await insert_new_user_in_table(user_id, user_name)
        await message.answer(text=f'{html.bold(html.quote(user_name))}, '
                                  f'{start}',
                             parse_mode=ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.delete()



@ch_router.message(PRE_START())
async def before_start(message: Message):
    prestart_ant = await message.answer(text='Klicken auf <b>start</b> !',
                                        reply_markup=pre_start_clava)
    await message.delete()
    await asyncio.sleep(3)
    await prestart_ant.delete()


@ch_router.message(IS_LETTER())
async def artikle_geber(message: Message):
    user_id = message.from_user.id
    suchend_word = message.text
    print(suchend_word.capitalize())
    art_kit = ('der', 'die', 'das')
    c = 0
    test_art = ''
    for art in art_kit:
        c += 1
        await asyncio.sleep(1)
        print('c = ', c)
        zapros = f'{site_url}{art}/{suchend_word.capitalize()}.html'

        req = requests.get(url=zapros, headers=site_headers)
        if req.status_code == 200:
            req.encoding = 'utf-8'
            test_art = art
            print(art)
            neue_wort = art + ' '+ message.text.strip().capitalize()
            if c == 1:
                await insert_neue_wort_in_der(user_id, neue_wort)
            elif c==2:
                await insert_neue_wort_in_die(user_id, neue_wort)
            else:
                await insert_neue_wort_in_das(user_id, neue_wort)

            soup = bs(req.text, 'lxml')
            english_gleiche = soup.find(class_='container text-center my-auto').find_all('span')

            plural_form = soup.find(class_='table')
            if plural_form:
                two_step_plural_form = plural_form.find_all('tr')

                full_nominative = two_step_plural_form[1]
                nur_plural = full_nominative.find_all('td')
                if nur_plural[2].text.strip() == '-':
                    plural_data = 'Nur Singular !'
                else:
                    plural_data = nur_plural[2].text
            else:
                plural_data = ''

            if len(english_gleiche) > 1:
                eng_analog = english_gleiche[1].text
                print('english_gleiche = ', english_gleiche)
                gleiche = eng_analog.split()[-1].capitalize()
                print('eng_analog.split()[-1] = ', eng_analog.split())

                if plural_data:
                    atw_satz = f'<b>{neue_wort};</b>  Plural Form  <b>{plural_data}</b>\n<b><i>English = {gleiche}</i></b>'
                    await message.answer(atw_satz)
                else:
                    atw_satz = f'<b>{neue_wort}</b>\n<b><i>English = {gleiche}</i></b>'
                    await message.answer(atw_satz)
            else:
                if plural_data:
                    atw_satz = f'<b>{neue_wort};</b>  Plural Form  <b>{plural_data}</b>'
                    await message.answer(atw_satz)
                else:
                    antwort = f'{neue_wort}'
                    await message.answer(antwort)

            # if len(english_gleiche)>1:
            #     eng_analog = english_gleiche[1].text
            #     print('english_gleiche = ', english_gleiche)
            #     gleiche = eng_analog.split()[1].capitalize()
            #     atw_satz = f'<b>{neue_wort}</b>\n<b><i>English = {gleiche}</i></b>'
            #     await message.answer(atw_satz)
            # else:
            #     await message.answer(f'<b>{neue_wort}</b>')
            break
    if test_art == '':
        att = await message.answer("Ich weiss nicht diesen Word")
        await asyncio.sleep(3)
        await att.delete()

    await message.delete()

@ch_router.message(Command('help'))
async def process_help_command(message: Message):
    att = await message.answer(text=help_text)
    await asyncio.sleep(10)
    await message.delete()
    await att.delete()



@ch_router.message(Command('zeigen'))
async def process_show_command(message: Message):
    print('INTO ZEIGEN')
    user_id = message.from_user.id
    der = await return_der_string(user_id)
    die = await return_die_string(user_id)
    das = await return_das_string(user_id)
    DER = await message.answer(der)
    DIE = await message.answer(die)
    DAS = await message.answer(das)
    await message.delete()



@ch_router.message()
async def delete_text_messages(message: Message):
    await message.delete()






