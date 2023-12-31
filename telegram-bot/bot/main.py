import os
import logging

from telegram.ext import ApplicationBuilder
from telegram.error import InvalidToken
from bot.handler import CommandHandler
from bot.cmdparser import create_parser
from bot.commands import Command, list_items, add_item

def run():
    APITOKEN = os.getenv('APITOKEN', None)
    if APITOKEN is None: raise EnvironmentError(f'env variable APITOKEN not found')

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    logging.getLogger('httpx').setLevel(logging.WARNING)

    parser = create_parser([
        Command.from_module('/add' , add_item),
        Command.from_module('/list', list_items),
    ])

    try:
        application = ApplicationBuilder().token(APITOKEN).build()
        application.add_handler(CommandHandler(parser))
        application.run_polling()

    except InvalidToken as e:
        raise EnvironmentError(f'Invalid token: {APITOKEN!r}')


if __name__ == '__main__': run()
