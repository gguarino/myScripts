#!/usr/bin/python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import paramiko, urllib, os
import botconfig as cfg
# import logging

#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def sshAction(bot, update):
    action=update.message.text

    if 'ledon' in action:
        scripto='/data/scripts/accendi.py'
    elif 'ledoff' in action:
        scripto='/data/scripts/spegni.py'	
    else:
        return False

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(cfg.server, port=cfg.port, username=cfg.username, password=cfg.password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(scripto)
    update.message.reply_text(ssh_stdout)

def screenshot(bot, update):
    imgDsk='/tmp/screenshot.jpg'
    urllib.urlretrieve(cfg.screenshoturl, imgDsk)
    update.message.reply_photo(photo=open(imgDsk, 'rb'))
    os.remove(imgDsk)


def dahelp(bot, update):
    update.message.reply_text('\n'.join(cfg.helpRows))


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Reply "+update.message.text)

updater = Updater(token=cfg.botToken)
unknown_handler = MessageHandler(Filters.text, unknown)


updater.dispatcher.add_handler(CommandHandler('help', dahelp))
updater.dispatcher.add_handler(CommandHandler('ledon', sshAction))
updater.dispatcher.add_handler(CommandHandler('ledoff', sshAction))
updater.dispatcher.add_handler(CommandHandler('screenshot', screenshot))
#updater.dispatcher.add_handler(unknown_handler)


updater.start_polling()
updater.idle()
