from telegram.ext import Updater, CommandHandler
from settings import TOKEN
from views import error_handler, help_view, list_view, exchange_view, history_view


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help_view))
    dp.add_handler(CommandHandler("list", list_view))
    dp.add_handler(CommandHandler("exchange", exchange_view))
    dp.add_handler(CommandHandler("history", history_view))

    dp.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
