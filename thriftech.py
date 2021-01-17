
# inf contains the bot's token
import inf

# discord.py
import discord
from discord.ext import commands

# The text adventure game loop
import game

# For the bot loop
from time import time, sleep
from asyncio import get_event_loop, Task, gather

thriftech = commands.Bot(command_prefix='.')
bot_id = 800102928911433818


@thriftech.event
async def on_ready():
    await thriftech.change_presence(activity=discord.Game('DM "help" to play!'))
    print('Connected')


@thriftech.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author.id != bot_id:
        print("processing message for user id %d: %s" % (message.author.id, message.content))
        raw = message.content.split(" ")
        for e in range(len(raw)):
            raw[e] = raw[e].lower()
        await message.author.send(game.run_command(message.author.id, raw))


# I took this from Zote, and it works so yay
fail_delay = 25
loop = get_event_loop()
while True:
    try:
        print("Initializing...")
        loop.run_until_complete(thriftech.start(inf.TOKEN))
    except Exception as exc:
        # Generic exception because I'm bad
        start = time()
        pending = Task.all_tasks(loop=thriftech.loop)
        gathered = gather(*pending, loop=thriftech.loop)
        try:
            gathered.cancel()
            thriftech.loop.run_until_complete(gathered)
            gathered.exception()
        except Exception:  # This could be better too
            pass
    print(f"Attempting restart in {fail_delay} seconds...")
    sleep(fail_delay)


