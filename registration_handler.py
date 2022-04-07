from lib2to3 import refactor
import logging
import datetime
from sklearn import tree
from sqlalchemy import false
from telegram import ReplyKeyboardMarkup, Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackContext, ConversationHandler
from typing import Dict


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

INIT_CHOISE, NAME, SURNAME, PHONE, QUANTITY, WINDOW = range(6)


def start_command(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Зареєструватися на сьогодні'], ['Зареєструватися на завтра']]
    update.message.reply_text(
        'Оберіть опцію:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    return INIT_CHOISE


def registration1(update: Update, context: CallbackContext) -> int:
    if datetime.datetime.now().strftime('%H:%M:%S') >= '18:00:00':
        reply_keyboard = [['Зареєструватися на сьогодні'], ['Зареєструватися на завтра']]
        update.message.reply_text(
            'Реєстрацію на сьогодні завершено. Ви можете зареєстуватися на завтра',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
            )
        )

        return INIT_CHOISE

    context.user_data['date'] = 'today'
    update.message.reply_text(
        'Ваше ім\'я:'
    )

    return NAME

    
def registration2(update: Update, context: CallbackContext) -> int:
    context.user_data['date'] = 'tomorrow'
    update.message.reply_text(
        'Ваше ім\'я:'
    )

    return NAME

def name(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['name'] = text

    update.message.reply_text(
        'Ваше прізвище:'
    )

    return SURNAME

def surname(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['surname'] = text

    update.message.reply_text(
        'Ваш номер телефону:'
    )

    return PHONE

def phone(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['phone_number'] = text

    update.message.reply_text(
        'Кількість людей: (REVIEW THIS)'
    )

    return QUANTITY

def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f'{value}' for _, value in user_data.items()]
    return "\n".join(facts[1:]).join(['\n', '\n'])

from booking_handler import read_booking_data, timestamps, write_booking_data

stamps_m = [timestamps[i:i+6] for i in range(0, len(timestamps), 6)]

keyboard = [
    [InlineKeyboardButton(stamp, callback_data=stamp) for stamp in stamps_m[0]],
     [InlineKeyboardButton(stamp, callback_data=stamp) for stamp in stamps_m[1]],
      [InlineKeyboardButton(stamp, callback_data=stamp) for stamp in stamps_m[2]]
]

inline_markup = InlineKeyboardMarkup(keyboard)

def quant(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['quantity'] = text

    update.message.reply_text(
        "Реєстрацію завершено." 
        f"{facts_to_str(context.user_data)}"       
        "Оберіть бажаний час:\n",
        reply_markup=inline_markup
    )

    return WINDOW


MAX_ENTRIES = 10

def check_entries(data, date, stamp, max):
    try:
        curr = data[date][stamp]
    except KeyError:
        return True
    
    if curr >= max:
        return False
    
    return True

def booking_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    stamp = query.data 
    u_data = context.user_data    
    
    current_data = read_booking_data()

    today = datetime.date.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

    date = today if u_data['date'] == 'today' else tomorrow

    query.edit_message_text(text=f'{facts_to_str(context.user_data)}\n'
                                 f'Обраний час: {date} {stamp}')

    if not check_entries(current_data, date, stamp, MAX_ENTRIES):
        query.edit_message_text(
                'Обраний час уже зайнято, оберіть інший.',
                reply_markup=inline_markup
            )
        return WINDOW
    else:
        write_booking_data(date, stamp, u_data['quantity'])

    return ConversationHandler.END







