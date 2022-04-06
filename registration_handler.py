import logging
import datetime
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
    return "\n".join(facts).join(['\n', '\n'])

def quant(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['quantity'] = text

    keyboard = [[InlineKeyboardButton(stamp, callback_data=callback)] for callback, stamp in stamp_map.items()]
    inline_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Реєстрацію завершено." 
        f"{facts_to_str(context.user_data)}"       
        "Оберіть бажаний час:\n",
        reply_markup=inline_markup
    )

    return WINDOW

from booking_handler import read_booking_data, timestamps, write_booking_data

stamp_map = dict(zip(
        list(range(len(timestamps))), 
        timestamps
        )
    )

MAX_ENTRIES = 10

def booking_callback__handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    stamp_index = int(query.data)
    stamp = stamp_map[stamp_index]

    query.edit_message_text(text=f"{facts_to_str(context.user_data)}\n"
                                 f'Обраний час: {stamp}')
    
    u_data = context.user_data

    if u_data['date'] == 'today':
        today = datetime.date.today().strftime("%d/%m/%Y")
        current_stamps = read_booking_data()
        try:
            if current_stamps[today][stamp] >= MAX_ENTRIES:
                keyboard = [[InlineKeyboardButton(stamp, callback_data=callback)] for callback, stamp in stamp_map.items()]
                inline_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(
                    'Обраний час уже зайнято, оберіть інший.',
                    reply_markup=inline_markup
                )
                return WINDOW
            else:
                write_booking_data(today, stamp, u_data['quantity'])
        except KeyError:
            current_stamps[today] = dict.fromkeys(timestamps, 0)
            if current_stamps[today][stamp] >= MAX_ENTRIES:
                keyboard = [[InlineKeyboardButton(stamp, callback_data=callback)] for callback, stamp in stamp_map.items()]
                inline_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(
                    'Обраний час уже зайнято, оберіть інший.',
                    reply_markup=inline_markup
                )
                return WINDOW
            else:
                write_booking_data(today, stamp, u_data['quantity'])

    elif u_data['date'] == 'tomorrow':
        print('ENTERED TOMMORROW REG')
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
        print(f'tommorow date: {tomorrow}')
        current_stamps = read_booking_data()

        try:
            if current_stamps[tomorrow][stamp] >= MAX_ENTRIES:
                keyboard = [[InlineKeyboardButton(stamp, callback_data=callback)] for callback, stamp in stamp_map.items()]
                inline_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(
                    'Обраний час уже зайнято, оберіть інший.',
                    reply_markup=inline_markup
                )
                return WINDOW
            else:
                write_booking_data(tomorrow, stamp, u_data['quantity'])
        except KeyError:
             current_stamps[tomorrow] = dict.fromkeys(timestamps, 0)
             if current_stamps[tomorrow][stamp] >= MAX_ENTRIES:
                keyboard = [[InlineKeyboardButton(stamp, callback_data=callback)] for callback, stamp in stamp_map.items()]
                inline_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(
                    'Обраний час уже зайнято, оберіть інший.',
                    reply_markup=inline_markup
                )
                return WINDOW
             else:
                write_booking_data(tomorrow, stamp, u_data['quantity'])
    return ConversationHandler.END







