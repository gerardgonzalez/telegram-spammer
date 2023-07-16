from telegram.telegram_module import *
from telegram.data.clients import clients
from telegram.telegram_spammer import TelegramSpammer

# TelegramSpammer instance
ts = TelegramSpammer()

# Connect clients
ts.start_clients(clients)

# Show menu
menu(ts)

