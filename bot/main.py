import os
import logging

from telegram.ext import ApplicationBuilder
from bot.handler import CommandHandler
from bot.cmdparser import create_parser
from bot.commands import Command, list_items, add_item

def run():
    APITOKEN = os.getenv('APITOKEN', None)
    if APITOKEN is None: raise EnvironmentError(f'env variable APITOKEN not found')

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    parser = create_parser([
        Command('/add' , add_item.help  , add_item.configure_parser  , add_item.handler),
        Command('/list', list_items.help, list_items.configure_parser, list_items.handler),
    ])

    application = ApplicationBuilder().token(APITOKEN).build()
    application.add_handler(CommandHandler(parser))
    application.run_polling()


if __name__ == '__main__': run()
