#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import youtube_dl
import requests
from redvid import Downloader
import subprocess

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

vredd = Downloader(max_q=True)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi! Send me a media link and I\'ll try to download it!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Just forward the link and let me do the rest!')


def echo(update, context):
    link = update.message.text.split('?')[0]
    data = requests.get(link+'.json', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'}).json()
    data = data[0]['data']['children'][0]['data']

    if data['url'].startswith('https://v.redd'):
        # v.reddit extractor
        vredd.url = data['url']
        file = vredd.download()
        update.message.reply_video(open(file, 'rb'), caption=data['title'])
        return

    elif data['url'].startswith('https://gfycat') or data['url'].startswith('https://redgifs'):
        # gfycat extractor
        url = requests.get(data['url'], allow_redirects=True).url
        urls = subprocess.check_output(['youtube-dl', '--quiet', url, '--exec', 'echo {}']).decode('UTF-8').strip()
        update.message.reply_video(open(urls, 'rb'), caption=data['title'])
        return
    
    elif data['url'].startswith('https://i.redd'):
        # i.reddit extractor
        update.message.reply_photo(data['url'], caption=data['title'])
        return

    elif data['url'].startswith('https://i.imgur') or data['url'].startswith('https://imgur'):
        # imgur extractor
        try:
            urls = subprocess.check_output(['imgur_downloader', '--print-only', data['url']]).decode('UTF-8').splitlines()
            for u in urls:
                if u.endswith('gifv'):
                    update.message.reply_video(u[:-4]+'mp4')
                else:
                    update.message.reply_photo(u)
        except:
            update.message.reply_message('Could not parse!')
        return

    else:
        update.message.reply_message('Could not parse!')
        return

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ['TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()