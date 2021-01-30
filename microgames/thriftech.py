import copy
import os
import json
import random

cmd = []
data = {}

# The save file format
_frame = {
    "computer":
        {
            "psu": False,
            "motherboard": False,
            "processor": False,
            "graphics card": False,
            "hard drive": False,
            "solid state drive": False,
            "ram": False
        },

    "inventory":
        {
            "glass": 0,
            "scrap metal": 0,
            "plastic": 0,
            "copper wire": 0,

            "circuit board": 0,
            "cable": 0,
            "microchip": 0,
            "capacitor": 0,
            "casing": 0,

            "psu": 0,
            "motherboard": 0,
            "processor": 0,
            "graphics card": 0,
            "hard drive": 0,
            "solid state drive": 0,
            "ram": 0,

            "computer": 0
        }
}

_materials = [
    "glass",
    "scrap metal",
    "plastic",
    "copper wire"
]

_parts = [
    "circuit board",
    "cable",
    "microchip",
    "capacitor",
    "casing"
]

_components = [
    "psu",
    "motherboard",
    "processor",
    "graphics card",
    "hard drive",
    "solid state drive",
    "ram"
]

part_recipes = {
    "circuit board": (("glass", 1), ("plastic", 1), ("copper wire", 1)),
    "cable": (("copper wire", 2), ("plastic", 1)),
    "microchip": (("scrap metal", 1), ("plastic", 1), ("glass", 1)),
    "capacitor": (("scrap metal", 1), ("copper wire", 1), ("glass", 1)),
    "casing": (("scrap metal", 2), ("plastic", 1), ("glass", 1))
}

component_recipes = {
    "psu": (("casing", 1), ("cable", 1), ("capacitor", 2)),
    "motherboard": (("circuit board", 2), ("cable", 1), ("microchip", 1)),
    "processor": (("microchip", 2), ("cable", 2), ("capacitor", 1)),
    "graphics card": (("casing", 1), ("microchip", 2), ("circuit board", 1)),
    "hard drive": (("casing", 1), ("circuit board", 1), ("cable", 2)),
    "solid state drive": (("casing", 1), ("circuit board", 1), ("microchip", 1)),
    "ram": (("microchip", 1), ("cable", 1), ("circuit board", 1))
}


# Load the save game. Performed at the beginning of each turn
def load(id_num):
    # Check for file
    file_name = "saves/thriftech/" + str(id_num) + ".json"
    if not os.path.exists("../saves/thriftech"):
        os.mkdir("../saves/thriftech")
    if os.path.exists(file_name):
        dat = {}
        with open(file_name, "r") as f:
            dat = json.load(f)
        return dat
    else:
        return copy.deepcopy(_frame)


# Save the game. Performed at the end of each turn
def save(id_num, dat):
    file_name = "saves/thriftech/" + str(id_num) + ".json"
    if not os.path.exists("../saves/thriftech"):
        os.mkdir("../saves/thriftech")
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


# See inventory and computer restoration progress
def show_stats():
    out = ""

    out += "**INVENTORY**\n"
    for each in data["inventory"]:
        if data["inventory"][each] > 0:
            out += "%s: %d" % (each, data["inventory"][each])
            out += "\n"
    out += "\n"

    out += "**COMPUTER**\n"
    for each in data["computer"]:
        if data["computer"][each]:
            out += "%s loaded" % each
            out += "\n"

    return out


# See help text
def show_help():
    out = "Welcome to ThrifTech, a text adventure crafting game!\n\n"

    out += "*PROCESS* trash to harvest crafting materials!\n\n"
    out += "*CRAFT PARTS* and *COMPONENTS* to *FIX* computers!\n\n"

    out += "Each computer needs one of each of the following items:\n"
    out += "-PSU\n"
    out += "-motherboard\n"
    out += "-processor\n"
    out += "-graphics card\n"
    out += "-hard drive\n"
    out += "-solid state drive\n"
    out += "-RAM\n\n"

    out += "Check your *STATS* to see your inventory and computer status!"

    return out


# Reset computer build progress to zero after completing a computer
def reset_computer():
    for each in data["computer"]:
        data["computer"][each] = False
    return True


# Check if the player has all ingredients for a given recipe
def has_all_ingredients(recipe):
    for mat in recipe:
        if data["inventory"][mat[0]] < mat[1]:
            return False

    # Since all materials are possessed, take
    # one of each material from inventory.
    # The crafted item is given outside this method
    for mat in recipe:
        data["inventory"][mat[0]] -= mat[1]

    return True


# Format recipe for inclusion in messages
def format_recipe(recipe):
    out = ""
    for each in recipe:
        out += "%s: %d / %d\n" % (each[0], data["inventory"][each[0]], each[1])
    return out


# Craft parts and components, or view crafting menus
def craft():

    # When the only thing said is 'craft'
    if len(cmd) == 1:
        out = "What would you like to craft?\n"
        out += "Say CRAFT PARTS or CRAFT COMPONENTS to see crafting menus."
        return out

    # Component-related commands
    for each in _components:
        # Craft a specific component
        if check_cmd("craft", *each.split(" ")):
            if has_all_ingredients(component_recipes[each]):
                data["inventory"][each] += 1
                return "You craft a %s" % each
            else:
                out = "You do not have all the required materials to craft a %s\n" % each
                out += format_recipe(component_recipes[each])
                return out
    # See component crafting menu
    if check_cmd("craft", ["component", "components"]):
        out = "**COMPONENT CRAFTING MENU**"
        for each in component_recipes.items():
            to_print = "**" + each[0] + "**\n"
            for mat in each[1]:
                to_print += mat[0] + ": "
                to_print += str(data["inventory"][mat[0]]) + "/"
                to_print += str(mat[1]) + ", "
            out += "\n" + to_print[:-2] + "\n"
        return out

    # Part-related commands
    for each in _parts:
        # Craft a specific part
        if check_cmd("craft", *each.split(" ")):
            if has_all_ingredients(part_recipes[each]):
                data["inventory"][each] += 1
                return "You craft a %s" % each
            else:
                out = "You do not have all the required materials to craft a %s\n" % each
                out += format_recipe(part_recipes[each])
                return out
    # See part crafting menu
    if check_cmd("craft", ["part", "parts"]):
        out = "**PART CRAFTING MENU**"
        for each in part_recipes.items():
            to_print = "**" + each[0] + "**\n"
            for mat in each[1]:
                to_print += mat[0] + ": "
                to_print += str(data["inventory"][mat[0]]) + "/"
                to_print += str(mat[1]) + ", "
            out += "\n" + to_print[:-2] + "\n"
        return out

    out = "What would you like to craft?\n"
    out += "Say CRAFT PARTS or CRAFT COMPONENTS to see crafting menus."
    return out


# Add computer components to computer
def fix():

    at_least_one_fixed = False
    for each in _components:
        if not data["computer"][each] and data["inventory"][each] > 0:
            data["computer"][each] = True
            data["inventory"][each] -= 1
            at_least_one_fixed = True

    if at_least_one_fixed:
        return "You add some components to the computer"
    else:
        return "You have no needed components"


# Process trash for materials
def process():
    out = ""
    for each in _materials:
        r = random.randint(0, 2)
        if r > 0:
            out += "You get %d %s\n" % (r, each)
            data["inventory"][each] += r

    if out == "":
        return "You get no materials. Unlucky!"

    return out


# Main loop for the game
def run_thriftech(id_num, cmd_string):
    global data
    data = load(id_num)
    print(id_num, data)

    global cmd
    cmd = cmd_string

    return_string = "Hint: PROCESS trash for raw materials!"

    if check_cmd("craft"):
        return_string = craft()
    elif check_cmd("stats"):
        return_string = show_stats()
    elif check_cmd("fix"):
        return_string = fix()
    elif check_cmd("process"):
        return_string = process()
    elif check_cmd("help"):
        return_string = show_help()

    # Check to see if a computer is fully built
    if all(data["computer"].values()):
        data["inventory"]["computer"] += 1
        reset_computer()
        return_string += "\nYou build a computer.\n"
        return_string += "You have now built %d computers." % data["inventory"]["computer"]

    save(id_num, data)

    return return_string
