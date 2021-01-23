# For loading config
import json

# inf contains the bot's token
import inf

# discord.py
import discord
from discord.ext import commands

# The text adventure game loop
from microgames import thriftech, stox

# For the bot loop
from time import time, sleep
from asyncio import get_event_loop, Task, gather


bot = commands.Bot(command_prefix='.')
bot_id = 800102928911433818

games = [
    thriftech.run_thriftech,
    stox.run_stox
]

# Load selected games for each player
game_id = {}

with open("config/game_id.json", "r") as f:
    game_id = json.load(f)


def about_text():
    output = "With this bot, you can play a variety of text-based games!\n"
    output += "Just type 'play [game name]' to select a game.\n"
    output += "Type 'help' for more information about the game!\n"
    output += "\n"
    output += "**GAMES**\n"
    output += "*ThrifTech*: process trash to build computers!\n"
    output += "*Stox*: Buy and sell for maximum profit!\n"
    return output


# Change and then save game ID file
def change_game_id(author_id, num):
    game_id[str(author_id)] = num
    with open("config/game_id.json", "w") as f:
        json.dump(game_id, f)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('DM "about" to learn more!'))
    print('Connected')


@bot.event
async def on_message(message):
    author = message.author
    if isinstance(message.channel, discord.DMChannel) and author.id != bot_id:
        print("processing message for user id %d: %s" % (author.id, message.content))
        raw = message.content.split(" ")
        for e in range(len(raw)):
            raw[e] = raw[e].lower()

        if str(author.id) not in game_id:
            game_id.update({str(author.id): 0})

        if raw[0] == "about":
            await author.send(about_text())
        elif raw[0] == "play" and raw[1] == "thriftech":
            change_game_id(author.id, 0)
            await author.send("You switch the game cartridge to ThrifTech.")
        elif raw[0] == "play" and raw[1] == "stox":
            change_game_id(author.id, 1)
            await author.send("You switch the game cartridge to Stox.")
        else:
            await author.send(games[game_id[str(author.id)]](author.id, raw))


# I took this from Zote, and it works so yay
fail_delay = 25
loop = get_event_loop()
while True:
    try:
        print("Initializing...")
        loop.run_until_complete(bot.start(inf.TOKEN))
    except Exception as exc:
        # Generic exception because I'm bad
        start = time()
        pending = Task.all_tasks(loop=bot.loop)
        gathered = gather(*pending, loop=bot.loop)
        try:
            gathered.cancel()
            bot.loop.run_until_complete(gathered)
            gathered.exception()
        except Exception:  # This could be better too
            pass
    print(f"Attempting restart in {fail_delay} seconds...")
    sleep(fail_delay)


