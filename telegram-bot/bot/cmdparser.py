from typing import List
import logging
import traceback
import argparse
import shlex

from telegram import Update
from telegram.ext import ContextTypes

from bot.commands import Command


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    ''' Callback for the showing global & command-specific help '''
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE, messages: List[str]) -> None:
    ''' Callback for informing about errors while parsing commands '''
    for message in messages:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = message
        )

# Exceptions to interrupt parsing & send info to the user
class ParserHelp(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class ParserError(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class CmdParser(argparse.ArgumentParser):
    ignore_args = {'command', 'handler', 'parser', 'help'}

    # Override error & print_help to generate interruptions
    def error(self, message: str, *args, **kwargs):
        raise ParserError(messages = [message, self.format_help()])

    def print_help(self, *args, **kwargs) -> None:
        raise ParserHelp(message = self.format_help())

    # Parse args for specific command or go directly to help & error handlers
    def parse_args(self, cmd: str) -> argparse.Namespace:
        try: return super().parse_args(shlex.split(cmd))
        except ParserHelp as e: return argparse.Namespace(handler=help, **e.kwargs)
        except ParserError as e: return argparse.Namespace(handler=error, **e.kwargs)

    # Fetch all arguments for the command exluding global ones
    @staticmethod
    def get_kwargs(args: argparse.Namespace) -> dict:
        return {name: value for name, value in vars(args).items() if name not in CmdParser.ignore_args}


# Create a parser for all the given commands & and a global help command
def create_parser(commands: List[Command]):
    parser = CmdParser(add_help=False, usage=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    for cmd in commands:
        try:
            if not cmd.init():
                logging.warning(f'{cmd} failed to intialize. Skipping binding')
                continue

        except Exception as e:
            logging.error(f'Error while initializing {cmd}. Skipping binding')
            logging.error('\n'.join(traceback.format_exc().splitlines()))
            continue

        subparser = subparsers.add_parser(cmd.name, help=cmd.help, usage=argparse.SUPPRESS)
        subparser.set_defaults(handler=cmd.handler)
        cmd.configure_parser(subparser)

    help_parser = subparsers.add_parser('/help', help='Show this help message', usage=argparse.SUPPRESS)
    help_parser.set_defaults(handler=help, message=parser.format_help())

    return parser

