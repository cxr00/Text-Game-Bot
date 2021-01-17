import inf
import discord
from discord.ext import commands
import game

from time import time, sleep
from asyncio import get_event_loop, Task, gather


thriftech = commands.Bot(command_prefix='.')
game_channel = 800127364289790002
bot_id = 800102928911433818


@thriftech.event
async def on_ready():
    print('Connected')


@thriftech.event
async def on_message(message):
    if message.channel.id == game_channel and message.author.id != bot_id:
        print("processing message: " + message.content)
        raw = message.content.split(" ")
        for e in range(len(raw)):
            raw[e] = raw[e].lower()
        chn = thriftech.get_channel(game_channel)
        await chn.send(game.run_command(message.author.id, raw))


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
        except Exception:  # This could be better
            pass
    print(f"Attempting restart in {fail_delay} seconds...")
    sleep(fail_delay)


