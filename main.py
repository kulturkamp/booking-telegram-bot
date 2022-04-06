from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,  CallbackQueryHandler, ConversationHandler
from registration_handler import INIT_CHOISE, NAME, PHONE, QUANTITY, SURNAME, WINDOW, booking_callback__handler, name, phone, quant, registration1, registration2, start_command, booking_callback__handler, surname

def main() -> None:
    with open('TOKEN', 'r') as f:
        token = f.read()
        updater = Updater(token)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            INIT_CHOISE:[
                MessageHandler(
                    Filters.regex('^Зареєструватися на сьогодні$'), registration1
                ),
                 MessageHandler(
                    Filters.regex('^Зареєструватися на завтра$'), registration2
                ),
            ],
            NAME:[
                MessageHandler(
                    Filters.text, name
                )
            ],
            SURNAME:[
                MessageHandler(
                    Filters.text, surname
                )
            ],
            PHONE:[
                MessageHandler(
                    Filters.text, phone
                )
            ],
            QUANTITY:[
                MessageHandler(
                    Filters.text, quant
                )
            ],
            WINDOW:[
                CallbackQueryHandler(booking_callback__handler)
            ]

        },
        fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()




if __name__ == '__main__':
    main()
