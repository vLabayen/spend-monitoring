import logging
from datetime import datetime as dt
from argparse import ArgumentParser

from telegram import Update
from telegram.ext import ContextTypes
from ndt.es7.core import scroll

from bot.utils.cmd_types import date
from bot.utils.elastic_q import range_q

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
    items = [hit['_source'] for r in scroll('items*', q, host='elastic') for hit in r['hits']['hits']]

    await context.bot.send_message(
        chat_id = update._effective_chat.id,
        text = '\n'.join('{date}: {name} - {cost}€'.format(
            date = dt.fromtimestamp(item['date']).strftime('%Y-%m-%d'),
            name = item['name'],
            cost = item['cost']
        ) for item in items)
	)