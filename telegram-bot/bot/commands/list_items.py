import logging
from datetime import datetime as dt
from argparse import ArgumentParser

from telegram import Update
from telegram.ext import ContextTypes
from ndt.es7.core import scroll, fetch_hits

from bot.utils.cmd_types import date
from bot.utils.elastic_q import range_q
from bot.domain.item import Item

help = 'List all the items in the bbdd'

def configure_parser(parser: ArgumentParser) -> None:
    parser.add_argument('--gte', type=date, metavar='date', default=None, help='Query start time')
    parser.add_argument('--lte', type=date, metavar='date', default=None, help='Query end time')

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, gte: dt, lte: dt) -> None:
    q = {
        'query': {'bool': {'filter': [
            range_q(gte, lte),
        ]}},
        'sort': [{'date': 'asc'}]
    }
    parse_hit = lambda hit: Item.from_dict(hit['_source'])
    items = [item for r in scroll('items*', q, host='elastic') for item in fetch_hits(r, parse_hit)]

    await context.bot.send_message(
        chat_id = update._effective_chat.id,
        text = '\n'.join(item.str_for_list() for item in items)
	)