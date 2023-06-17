import logging
import re
from datetime import datetime as dt
from ndt.time_handler import rtime2datetime

from argparse import ArgumentParser
from telegram import Update
from telegram.ext import ContextTypes

help = 'Add an item to the store'

date_rgx = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
def date(date: str) -> dt:
    if date_rgx.match(date): return dt.strptime(date, '%Y-%m-%d-%H-%M-%S')
    return rtime2datetime(date)

def configure_parser(parser: ArgumentParser) -> None:
	parser.add_argument('item', type=str, help='%(type)s: Name of the item')
	parser.add_argument('cost', type=float, help='%(type)s: Cost of the item in €')
	parser.add_argument('-d', '--date', type=date, help='%(type)s: Cost of the item in €', default=dt.now())

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, item: str, cost: float, date: dt) -> None:
    ''' Callback for the /add command.
    Add an item to the bbdd
    '''
    logging.info(f'Adding {item!r} with cost {cost} at time {date}')
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Added!'
    )
