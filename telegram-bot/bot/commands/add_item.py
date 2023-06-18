from typing import Union
import logging
import traceback
import json
from datetime import datetime as dt
from argparse import ArgumentParser

from telegram import Update
from telegram.ext import ContextTypes
from ndt.es7.core import index_document, QueryError
from ndt.es7.utils import ensure_index_and_mapping

from bot.utils.cmd_types import date
from bot.domain.item import Item
from bot.config.elastic import items_index_pattern, items_index, host as es_host

help = 'Add an item to the store'

def init() -> bool:
    ensure_index_and_mapping(items_index_pattern, Item.mapping(), host=es_host)
    return True

def configure_parser(parser: ArgumentParser) -> None:
	parser.add_argument('name', type=str  , help='%(type)s: Name of the item')
	parser.add_argument('cost', type=float, help='%(type)s: Cost of the item in €')
	parser.add_argument('-d', '--date'         , type=date, metavar='date'         , help='%(type)s: Purchase date'         , default=dt.now())
	parser.add_argument('-c', '--category'     , type=str , metavar='category'     , help='%(type)s: Category of the item'  , default=None)
	parser.add_argument('-e', '--establishment', type=str , metavar='establishment', help='%(type)s: Purchase establishment', default=None)

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, cost: float, date: dt, category: Union[str, None], establishment: Union[str, None]) -> None:
    ''' Callback for the /add command. Add an item to the bbdd '''
    item = Item(name, cost, date, category=category, establishment=establishment)

    try: index_document(items_index(), item.to_dict(), host=es_host)
    except QueryError as e:
        logging.error(f'Error indexing {item}: {json.dumps(str(e), indent=2)}')
        await context.bot.send_message(
             chat_id = update.effective_chat.id,
             text = f'Error adding item: {json.dumps(str(e), indent=2)}'
        )
        return

    except Exception as e:
         logging.error(f'Unexpected error: {str(e)}')
         logging.error('\n'.join(traceback.format_exc().splitlines()))
         await context.bot.send_message(
              chat_id = update.effective_chat.id,
              text = f'Unexpected error: {str(e)}'
         )
         return

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Added {item.to_json(indent=2)}'
    )
