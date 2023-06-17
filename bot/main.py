import os
import logging
import argparse

from telegram.ext import ApplicationBuilder
from bot.handler import CommandHandler
from bot.cmdparser import HelpAction, CmdParser
from bot.callbacks import (
    help,
    add,
)

def create_parser():
    parser = CmdParser(add_help=False, usage=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    add_parser = subparsers.add_parser('/add', help='Add an item to the store', add_help=False, usage=argparse.SUPPRESS)
    add_parser.set_defaults(handler=add)
    add_parser.add_argument('-h', '--help', action=HelpAction)
    add_parser.add_argument('item', type=str, help='%(type)s: Name of the item')
    add_parser.add_argument('cost', type=float, help='%(type)s: Cost of the item in €')

    help_parser = subparsers.add_parser('/help', help='Show this help message', add_help=False, usage=argparse.SUPPRESS)
    help_parser.set_defaults(handler=help, message=parser.format_help())
    help_parser.add_argument('-h', '--help', action=HelpAction)

    return parser

def run():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    APITOKEN = os.getenv('APITOKEN', None)
    if APITOKEN is None: raise EnvironmentError(f'env variable APITOKEN not found')

    application = ApplicationBuilder().token(APITOKEN).build()
    application.add_handler(CommandHandler(create_parser()))
    application.run_polling()


if __name__ == '__main__': run()
