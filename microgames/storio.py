import os
import json
import copy
import random

cmd = []
data = {}

_frame = {
    "credits": 50,
    "stock":
        {
            "plunger": 1,
            "tea": 3,
            "cheese": 2,
            "wine": 3,
            "lip balm": 4
        },
    "state": "exit"
}

price = {
    "plunger": 10,
    "tea": 20,
    "cheese": 15,
    "wine": 25,
    "lip balm": 12
}

items = [
    "plunger",
    "tea",
    "cheese",
    "wine",
    "lip balm"
]


def reset_stats():
    global data
    data = copy.deepcopy(_frame)
    return "You reset your stats.\n"


def show_stats():
    return_string = "credits: %d\n" % data["credits"]
    return_string += "ITEM STOCK:\n"
    for each in items:
        return_string += "%s: %d\n" % (each, data["stock"][each])
    return return_string


def show_help():
    return_string = "**How to play Storio**\n\n"

    return_string += "Customers will come in to browse your inventory.\n"
    return_string += "Your job is to ORDER goods to keep your inventory stocked for purchase.\n"
    return_string += "You keep a stock of PLUNGERS, TEA, CHEESE, WINE, and LIP BALM.\n"
    return_string += "If you run out of an item, you may miss out on that sweet, sweet profit.\n"
    return_string += "So be sure to type STATS so you know which items to order!\n"
    return_string += "Good luck!\n\n"

    return return_string


# Load the save game. Performed at the beginning of each turn
def load(id_num):
    # Check for file
    file_name = "saves/storio/" + str(id_num) + ".json"
    if not os.path.exists("../saves/storio"):
        os.mkdir("../saves/storio")
    if os.path.exists(file_name):
        dat = {}
        with open(file_name, "r") as f:
            dat = json.load(f)
        return dat
    else:
        return copy.deepcopy(_frame)


# Save the game. Performed at the end of each turn
def save(id_num, dat):
    file_name = "saves/storio/" + str(id_num) + ".json"
    if not os.path.exists("../saves/storio"):
        os.mkdir("../saves/storio")
    with open(file_name, "w+") as f:
        json.dump(dat, f)


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


def customer_purchase():
    global data

    return_string = ""

    item = items[random.randint(0, len(items) - 1)]

    if data["stock"][item] > 0:
        data["stock"][item] -= 1
        sell_price = round(price[item] * 1.25)
        data["credits"] += sell_price
        return_string += "The customer purchases a %s for %d credits.\n" % (item, sell_price)
    else:
        return_string += "The customer wants to purchase a %s, but you have none in stock.\n" % item

    return return_string


def order():
    return_string = ""
    for item in items:
        if check_cmd(["order", "buy"], *item.split(" ")):
            if data["credits"] >= price[item]:
                data["stock"][item] += 1
                data["credits"] -= price[item]
                return_string += "You order a %s for %d credits.\n" % (item, price[item])
            else:
                return_string += "You cannot afford the %s.\n" % item
            break
    return return_string


# Run the main game loop for one turn
def run_storio(id_num, cmd_string):
    global data
    data = load(id_num)
    print(id_num, data)

    global cmd
    cmd = cmd_string

    return_string = ""

    if check_cmd(["stats", "stock", "inventory"]):
        return_string += show_stats()
    elif check_cmd("help"):
        return_string += show_help()

    if data["state"] == "enter":
        return_string += "A customer enters the shop.\n"
        data["state"] = "in shop"
    if data["state"] == "in shop":
        return_string += "The customer is browsing.\n"
        if random.randint(0, 10) >= 4:
            return_string += customer_purchase()
        leaves = random.randint(0, 10) >= 5
        if leaves:
            data["state"] = "exit"
    if data["state"] == "exit":
        return_string += "The customer leaves the shop.\n"
        data["state"] = "enter"

    if check_cmd(["order", "buy"]):
        return_string += order()

    save(id_num, data)

    return return_string
