import re
from decimal import Decimal

from services import get_or_create_actual_rate_instance, history_service

import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def help_view(update, context):
    update.message.reply_text(
        """
    > /list - list of all available currencies\n> /exchange - convert currencies\n        example: `/exchange 10.00 USD to RUB`\n> /history - showing graph with currency rates in specified interval in days\n        example: /history USD/CAD for 100 days"""
    )


def list_view(update, context):
    instance = get_or_create_actual_rate_instance()
    response_data = [f'{key}: {Decimal(value).quantize(Decimal(".00"))}' for key, value in instance.rates.items()]
    response_data.append(f"updated in {instance.created_date}")
    update.message.reply_text("\n".join(response_data))


def exchange_view(update, context):
    rates = get_or_create_actual_rate_instance().rates
    try:
        source, target_currency = (
            update.message.text.replace("/exchange", "").replace(" ", "").replace(",", ".").split("to")
        )
        source_quantity = re.findall(r"\d+\.\d+", source) or re.findall(r"\d+", source)
        source_quantity = source_quantity[0]
        source_currency = source[-3:]
        target_currency_value = (
            Decimal(rates[target_currency]) * Decimal(source_quantity) / Decimal(rates[source_currency])
        ).quantize(Decimal(".00"))
        update.message.reply_text(f"{target_currency_value} {target_currency}")
    except (KeyError, TypeError, ValueError):
        update.message.reply_text(f"incorrect request, look /help for example")


def history_view(update, context):
    message = update.message.text.replace("/history", "")
    currencies, raw_interval = message.replace(" ", "").split("for")
    base_curr, targ_curr = currencies.split("/")
    interval_in_days = int(re.findall(r"\d+", raw_interval)[0])

    result = history_service(interval=interval_in_days, base=base_curr, symbol=targ_curr, graph_title=message)
    if result.get("error"):
        update.message.reply_text(result["error"])
    else:
        with open(result["file_name"], "rb") as image:
            update.message.chat.send_photo(photo=image)


def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
