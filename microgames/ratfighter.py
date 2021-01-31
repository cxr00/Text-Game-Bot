import os
import json
import copy
import random

cmd = []
data = {}

_frame = {
    "in battle": False,
    "stats": {
        "max health": 5,
        "current health": 5,
        "weapon": 2,
        "armor": 0,
        "accessory": 2,
        "credits": 2,
        "points": 0
    },
    "enemy": {

    }
}

# Stats are [health, weapon, armor, payout]
_rats = {
    "sewer rat": [5, 1, 0, 1],
    "dire rat": [9, 2, 1, 2],
    "forest rat": [15, 4, 2, 3],
    "were rat": [25, 7, 4, 5],
    "cyborg rat": [40, 12, 7, 8]
}


def reset_stats():
    """
    Reset the player's progress except for points earned
    """
    global data
    pts = data["stats"]["points"]
    data = copy.deepcopy(_frame)
    data["stats"]["points"] = pts


def help():
    return_string = "Welcome to RatFighter!\n\n"
    return_string += "FIGHT rats to earn credits for STATS upgrades.\n"
    return_string += "Visit the SHOP to UPGRADE your stats.\n"
    return_string += "Your WEAPON determines how much damage you deal.\n"
    return_string += "Your ARMOR determines how much damage you absorb.\n"
    return_string += "Your ACCESSORY determines how many credits you get for defeating rats.\n\n"
    return return_string


def stats():
    global data
    return_string = "**PLAYER STATS**\n\n"
    return_string = "HEALTH: %d / %d\n" % (data["stats"]["current health"], data["stats"]["max health"])
    return_string += "WEAPON: %d\n" % data["stats"]["weapon"]
    return_string += "ARMOR: %d\n" % data["stats"]["armor"]
    return_string += "ACCESSORY: %d\n" % data["stats"]["accessory"]
    return_string += "CREDITS: %d\n" % data["stats"]["credits"]
    return_string += "POINTS: %d" % data["stats"]["points"]
    return return_string


def enemy_stats():
    global data
    return_string = "**RAT STATS**\n"
    return_string += "HP: %d\n" % data["enemy"][0]
    return_string += "WEP: %d\n" % data["enemy"][1]
    return_string += "ARM: %d\n" % data["enemy"][2]
    return_string += "PAY: %d\n" % data["enemy"][3]
    return return_string


def shop_menu():
    return_string = "**SHOP UPGRADES**\n\n"
    return_string += "HEALTH: 3 credits\n"
    return_string += "WEAPON: 5 credits\n"
    return_string += "ARMOR: 3 credits\n"
    return_string += "ACCESSORY: 2 credits\n\n"
    return_string += "You have %d credits. What would you like to BUY?" % data["stats"]["credits"]
    return return_string


def fight_menu():
    return_string = "**SELECT AN OPPONENT**\n\n"
    return_string += "sewer rat: level 1\n"
    return_string += "dire rat: level 2\n"
    return_string += "forest rat: level 4\n"
    return_string += "were rat: level 7\n"
    return_string += "cyborg rat: level 12\n\n"
    return_string += "Choose which opponent to FIGHT."
    return return_string


# Load the save game. Performed at the beginning of each turn
def load(id_num):
    # Check for file
    file_name = "saves/ratfighter/" + str(id_num) + ".json"
    if not os.path.exists("../saves/ratfighter"):
        os.mkdir("../saves/ratfighter")
    if os.path.exists(file_name):
        dat = {}
        with open(file_name, "r") as f:
            dat = json.load(f)
        return dat
    else:
        return copy.deepcopy(_frame)


# Save the game. Performed at the end of each turn
def save(id_num, dat):
    file_name = "saves/ratfighter/" + str(id_num) + ".json"
    if not os.path.exists("../saves/ratfighter"):
        os.mkdir("../saves/ratfighter")
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


def shop():
    """
    BUY/UPGRADE your stats in exchange for CREDITS.

    :return: the result of your buy/upgrade command
    """
    global data
    if check_cmd(["upgrade", "buy"], ["health", "hp"]):
        if data["stats"]["credits"] >= 3:
            data["stats"]["credits"] -= 3
            data["stats"]["max health"] += 1
            data["stats"]["current health"] += 1
            return "You upgrade your health."
        else:
            return "You cannot afford to upgrade your health."
    elif check_cmd(["upgrade", "buy"], "weapon"):
        if data["stats"]["credits"] >= 5:
            data["stats"]["credits"] -= 5
            data["stats"]["weapon"] += 1
            return "You upgrade your weapon."
        else:
            return "You cannot afford to upgrade your weapon."
    elif check_cmd(["upgrade", "buy"], "armor"):
        if data["stats"]["credits"] >= 3:
            data["stats"]["credits"] -= 3
            data["stats"]["armor"] += 1
            return "You upgrade your armor."
        else:
            return "You cannot afford to upgrade your armor."
    elif check_cmd(["upgrade", "buy"], ["accessory", "acc"]):
        if data["stats"]["credits"] >= 2:
            data["stats"]["credits"] -= 2
            data["stats"]["accessory"] += 1
            return "You upgrade your accessory."
        else:
            return "You cannot afford to upgrade your accessory."

    return shop_menu()


def select_fight():
    global data

    # Iterate through rats to find one which matches the command
    for each in _rats:
        if check_cmd(["fight", "battle"], *each.split(" ")):
            data["in battle"] = True
            data["enemy"] = copy.deepcopy(_rats[each])
            return "You begin a battle with a %s." % each

    # Return fight menu by default
    return fight_menu()


def attack():
    global data

    return_string = "You attack the rat."

    # Player's attack
    attack_damage = data["stats"]["weapon"] - data["enemy"][2]
    if attack_damage < 0:
        attack_damage = 0
    data["enemy"][0] -= attack_damage
    return_string += "You deal %d damage\n" % attack_damage

    # Enemy's attack if it is still alive
    if data["enemy"][0] > 0:
        return_string += "The rat attacks you back.\n"
        attack_damage = data["enemy"][1] - data["stats"]["armor"]
        if attack_damage < 0:
            attack_damage = 0
        data["stats"]["current health"] -= attack_damage
        return_string += "It deals %d damage to you.\n" % attack_damage

    # Check if player is dead
    if data["stats"]["current health"] <= 0:
        data["in battle"] = False
        return_string += "The rat defeats you! You have been slain.\n"
        return_string += "Your progress has been reset."
        reset_stats()
    # Check if the enemy is dead
    elif data["enemy"][0] <= 0:
        data["in battle"] = False
        reward = random.randint(1, data["stats"]["accessory"]) + data["enemy"][3]
        data["stats"]["credits"] += reward
        data["stats"]["points"] += data["enemy"][3]
        return_string += "You defeat the rat! You are awarded %d credits and %d points" % (reward, data["enemy"][3])
        data["stats"]["current health"] = data["stats"]["max health"]

    return return_string


def run_ratfighter(id_num, cmd_string):
    global data
    data = load(id_num)
    print(id_num, data)

    global cmd
    cmd = cmd_string

    return_string = ""

    if data["in battle"]:
        return_string = "MENU:\tATTACK\tLOOK\tRUN"
        if check_cmd(["fight", "battle", "attack"]):
            return_string = attack()
        elif check_cmd(["look", "view"]):
            return_string = enemy_stats()
        elif check_cmd(["flee", "run"]):
            return_string = "You run away from the rat."
            data["in battle"] = False
    else:
        return_string = "HINT: Type 'help' to learn more!"
        if check_cmd(["fight", "battle"]):
            return_string = select_fight()
        elif check_cmd(["buy", "upgrade"]):
            return_string = shop()
        elif check_cmd("shop"):
            return_string = shop_menu()
        elif check_cmd("stats"):
            return_string = stats()
        elif check_cmd("help"):
            return_string = help()
        elif check_cmd("reset"):
            reset_stats()
            return_string = "You reset your progress."

    save(id_num, data)

    return return_string
