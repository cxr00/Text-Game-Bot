import copy
import os
import json
from random import randint, random
from math import ceil

cmd = []
data = {}
PROCESS_DAY = False

_frame = {
    "credits": 100.00,
    "stox":
        {
            "cxr": 0,
            "vlt": 0,
            "zot": 0,
            "nem": 0
        },
    "day price":
        {
            "cxr": 10,
            "vlt": 10,
            "zot": 10,
            "nem": 10
        },
    "previous day price":
        {
            "cxr": 0,
            "vlt": 0,
            "zot": 0,
            "nem": 0
        }
}

stox = [
    "cxr",
    "vlt",
    "zot",
    "nem"
]


# Load the save game. Performed at the beginning of each turn
def load(id_num):
    # Check for file
    file_name = "saves/stox/" + str(id_num) + ".json"
    if not os.path.exists("../saves/stox"):
        os.mkdir("../saves/stox")
    if os.path.exists(file_name):
        dat = {}
        with open(file_name, "r") as f:
            dat = json.load(f)
        return dat
    else:
        return copy.deepcopy(_frame)


# Save the game. Performed at the end of each turn
def save(id_num, dat):
    file_name = "saves/stox/" + str(id_num) + ".json"
    if not os.path.exists("saves/stox"):
        os.mkdir("saves/stox")
    with open(file_name, "w+") as f:
        json.dump(dat, f)


# Reset the save file
def reset_stox():
    global data
    data = copy.deepcopy(_frame)


# Rounds all values to the nearest tenth
def round_everything():
    global data
    data["credits"] = round(data["credits"], 1)
    for each in stox:
        data["stox"][each] = round(data["stox"][each], 1)
        data["day price"][each] = round(data["day price"][each], 1)
        data["previous day price"][each] = round(data["previous day price"][each], 1)


# Update the day price and previous day price
def process_day():
    for each in stox:
        data["previous day price"][each] = data["day price"][each]
        positive = True if random() < .5 else False
        stonk_change = ceil(random() * 10) / 10 + randint(0, 5)
        if stonk_change > data["day price"][each]:
            data["day price"][each] += stonk_change
        else:
            data["day price"][each] += stonk_change * (1 if positive else -1)
        data["day price"][each] = data["day price"][each]
    round_everything()


# Validates input as in-game commands
def check_cmd(*args):
    """
    Determines if command matches args

    :param args: To match to the command
    :return: Whether args matches command
    """

    def arg_matches_cmd(n):
        # Synonym engine
        # Returns False if there is not at least one match
        if isinstance(args[n], list):
            if not cmd[n] in args[n]:
                return False
        # For when cmd[n] is a single word
        elif cmd[n] != args[n].lower():
            return False
        return True

    # If the command is not at least as long as the args, it is obviously False
    if len(cmd) < len(args):
        return False

    for n in range(len(args)):
        if not arg_matches_cmd(n):
            return False

    return True


# Show the help string
def show_help():
    return_string = "Welcome to Stox!\n"
    return_string += "BUY and SELL stox for maximum profit!\n\n"

    return_string += "Each day the price of all stox will go up or down.\n"
    return_string += "Use your best judgment to decide when to sell!\n\n"

    return_string += "Type 'buy [stox name] [amount]' to buy.\n"
    return_string += "Type 'sell [stox name] [amount]' to sell."

    return return_string


# Show the player's stats
def show_stats():
    return_string = "**CREDITS:** %d\n\n" % data["credits"]
    return_string += "**YOUR STOX**\n"
    for each in stox:
        return_string += "%s: %d" % (each, data["stox"][each]) + "\n"

    return return_string


# Attempt to sell stox
def sell():
    # Check for valid stox name
    try:
        sell_stock = cmd[1]
    except IndexError:
        return "Which stox you want to sell?"
    valid_stock = False
    for each in stox:
        if sell_stock == each:
            valid_stock = True

    if not valid_stock:
        return "%s is not a valid stox" % sell_stock

    # Check for valid number
    try:
        amount = int(cmd[2])
    except IndexError:
        return "What number of stox do you want to sell?"
    except ValueError:
        return "%s is not a number.\nWhat number of stox do you want to sell?"

    # Check that you have enough credits
    if data["stox"][sell_stock] < amount:
        return "You do not have that many %s stox to sell" % sell_stock

    # Make sale
    data["credits"] += amount * data["day price"][sell_stock]
    data["credits"] = ceil(data["credits"] * 10) / 10
    data["stox"][sell_stock] -= amount

    # Trigger day to process
    global PROCESS_DAY
    PROCESS_DAY = True
    return "You sell %d %s stox." % (amount, sell_stock)


# Attempt to buy stox
def buy():

    # Check for valid stox name
    try:
        buy_stock = cmd[1]
    except IndexError:
        return "Which stox you want to buy?"
    valid_stock = False
    for each in stox:
        if buy_stock == each:
            valid_stock = True

    if not valid_stock:
        return "%s is not a valid stox" % buy_stock

    # Check for valid number
    try:
        amount = int(cmd[2])
    except IndexError:
        return "What number of stox do you want to buy?"
    except ValueError:
        return "%s is not a number. What number of stox do you want to buy?" % cmd[2]

    # Check that you have enough credits
    if data["credits"] < amount * data["day price"][buy_stock]:
        return "You cannot afford that many %s stox" % buy_stock

    # Make purchase
    data["credits"] -= amount * data["day price"][buy_stock]
    data["credits"] = ceil(data["credits"] * 10) / 10
    data["stox"][buy_stock] += amount

    # Trigger day to process
    global PROCESS_DAY
    PROCESS_DAY = True
    return "You buy %d %s stox." % (amount, buy_stock)


def run_stox(id_num, cmd_string):
    # Load player's data
    global data
    data = load(id_num)
    print(data)

    # Register command string to global variable
    global cmd
    cmd = cmd_string

    # Reset PROCESS_DAY
    global PROCESS_DAY
    PROCESS_DAY = False

    # Set return string to default value
    return_string = "Hint: Say 'help' to learn command syntax!"

    if check_cmd("sell"):
        return_string = sell()
    elif check_cmd("buy"):
        return_string = buy()
    elif check_cmd("reset"):
        reset_stox()
        return_string = "You reset the game."
    elif check_cmd("stats"):
        return_string = show_stats()
    elif check_cmd("help"):
        return_string = show_help()

    if PROCESS_DAY:
        process_day()

    # Save player's data
    save(id_num, data)

    return_string += "\n\n"

    # Add stox ticker and credits to return string
    for each in stox:
        return_string += each + ": "
        return_string += str(data["day price"][each])
        return_string += " / "

        price_change = data["day price"][each] - data["previous day price"][each]
        if price_change > 0:
            return_string += "+"
        return_string += str(price_change)
        return_string += " / "
        return_string += "(%d owned)" % data["stox"][each]

        return_string += "\n"
    return_string += "credits: %d" % data["credits"]

    return return_string
