"Crime and punishment, punishment and crime"

__version__ = "0.69.420"

import os
import re
import sys
import logging
from random import sample
import discord

LOGGER = logging.getLogger(__name__)
CLIENT = discord.Client()
TOKEN = os.getenv('INCEL2_DISCORD_TOKEN')
IMGROOT = os.getenv('INCEL2_DISCORD_IMGROOT')
EXTS = os.getenv('INCEL2_DISCORD_EXTS')
CAPTIONS = os.getenv('INCEL2_DISCORD_CAPTIONS')
REGEX = re.compile(f".*({EXTS})")


def pickpic():
    "Pick a random image from IMGROOT."
    return os.path.join(
        IMGROOT,
        sample([f for f in os.listdir(IMGROOT) if REGEX.match(f)], 1)[0]
    )


@CLIENT.event
async def on_ready():
    LOGGER.info('We have logged in as {0.user}\n'.format(CLIENT))


async def send_random_pic(message):
    if message.content.startswith('!i2'):
        logging.info(f"Responding to `{message.content}' on channel "
                     f"{message.channel} and guild {message.guild}...")
        f = pickpic()
        logging.info("Sending file: %s", f)
        s = os.stat(f).st_size
        if s > 5e5:
            logging.info("File is large (%s kB), warning user...", s)
            await message.channel.send("Found a big'n, friend... just a sec...")
        await message.channel.send(file=discord.File(f))
        return True  # handled by sending message
    else:
        return False


async def post_1(message):
    if message.content == "1":
        logging.info("Someone posted 1! Responding in kind...")
        await message.channel.send("1")
        return True
    return False


async def punish_imperfect_1(message):
    if message.content != "1":
        msg = f"Monadic blasphaemer detected: {message.author.name}"
        logging.info(msg)
        for snitch in [c for c in message.guild.channels if c.name == "pequod"]:
            await snitch.send(msg)
        return True
    return False


@CLIENT.event
async def on_message(message):
    if message.author == CLIENT.user:
        return

    if message.guild.name == "Mother Based":
        if message.channel.name == "i2-memorial":
            await send_random_pic(message)
        elif message.channel.name == "1-chat":
            await post_1(message)
            await punish_imperfect_1(message)
    else:
        await send_random_pic(message)


def main():
    logging.basicConfig(level='INFO')
    LOGGER.info('Starting Incellecual 2 Discord Server...')
    CLIENT.run(TOKEN)
    LOGGER.info('Shutting down... banned again :(')


if __name__ == '__main__':
    main()
