from typing import List
import logging

from telegram import Update
from telegram.ext import ContextTypes

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    ''' Callback for the /help command.
    Show global application help
    '''
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

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE, item: str, cost: float) -> None:
    ''' Callback for the /add command.
    Add an item to the bbdd
    '''
    logging.info(f'Adding {item!r} with cost {cost}')
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Added!'
    )
