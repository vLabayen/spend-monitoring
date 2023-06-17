import logging

from argparse import ArgumentParser
from telegram import Update
from telegram.ext import ContextTypes

help = 'Add an item to the store'

def configure_parser(parser: ArgumentParser) -> None:
	parser.add_argument('item', type=str, help='%(type)s: Name of the item')
	parser.add_argument('cost', type=float, help='%(type)s: Cost of the item in €')

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, item: str, cost: float) -> None:
    ''' Callback for the /add command.
    Add an item to the bbdd
    '''
    logging.info(f'Adding {item!r} with cost {cost}')
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Added!'
    )
