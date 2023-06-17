from typing import List
import logging

from argparse import ArgumentParser
from telegram import Update
from telegram.ext import ContextTypes

help = 'List the given items'

def configure_parser(parser: ArgumentParser) -> None:
	parser.add_argument('items', type=str, nargs='+', help='%(type)s: List of items to echo back')

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, items: List[str]) -> None:
    await context.bot.send_message(
        chat_id = update._effective_chat.id,
        text = '\n'.join(items)
	)