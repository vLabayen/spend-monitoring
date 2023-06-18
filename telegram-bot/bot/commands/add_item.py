from typing import Union
import logging
import json
from datetime import datetime as dt
from argparse import ArgumentParser

from telegram import Update
from telegram.ext import ContextTypes
from ndt.es7.core import index_document, QueryError

from bot.utils.cmd_types import date
from bot.domain.item import Item

help = 'Add an item to the store'

def configure_parser(parser: ArgumentParser) -> None:
	parser.add_argument('name', type=str  , help='%(type)s: Name of the item')
	parser.add_argument('cost', type=float, help='%(type)s: Cost of the item in €')
	parser.add_argument('-d', '--date'         , type=date, metavar='date'         , help='%(type)s: Purchase date'         , default=dt.now())
	parser.add_argument('-c', '--category'     , type=str , metavar='category'     , help='%(type)s: Category of the item'  , default=None)
	parser.add_argument('-e', '--establishment', type=str , metavar='establishment', help='%(type)s: Purchase establishment', default=None)

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, cost: float, date: dt, category: Union[str, None], establishment: Union[str, None]) -> None:
    ''' Callback for the /add command.
    Add an item to the bbdd
    '''
    item = Item(name, cost, date, category=category, establishment=establishment)

    try: index_document(f'items+{dt.now().year}', item.to_dict(), host='elastic')
    except QueryError as e:
        logging.error(f'Error indexing {item}: {json.dumps(str(e), indent=2)}')
        await context.bot.send_message(
             chat_id = update.effective_chat.id,
             text = f'Error adding item: {json.dumps(str(e), indent=2)}'
        )

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Added {item.to_json(indent=2)}'
    )
