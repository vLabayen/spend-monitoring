from typing import Union, Literal
import logging
import traceback
from argparse import Namespace

from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext._handler import BaseHandler
from telegram.ext._utils.types import CCT

from bot.cmdparser import CmdParser

logger = logging.getLogger(__name__)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.handler(update, context, **context.kwargs)

class CommandHandler(BaseHandler[Update, CCT]):
    __slots__ = ('parser', )

    def __init__(self, command_parser: CmdParser, block: bool = True):
        super().__init__(handle, block)
        self.parser = command_parser

    def check_update(self, update: object) -> Union[Literal[False], Namespace]:
        if not isinstance(update, Update): return False
        if not update.effective_message.text: return False

        logger.info(f'Received message: {update.effective_message.text!r}')

        try: return self.parser.parse_args(update.effective_message.text)
        except:
            logger.error('\n'.join(traceback.format_exc().splitlines()))
            return False

    def collect_additional_context(self, context: CCT, update: Update, application, args: Namespace) -> None:
        context.handler = args.handler
        context.kwargs = CmdParser.get_kwargs(args)
