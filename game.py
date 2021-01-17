import copy
import os
import json
import random

cmd = []
data = {}

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
    "psu": (("casing", 1), ("cable", 2), ("capacitor", 3)),
    "motherboard": (("circuit board", 2), ("cable", 1), ("microchip", 1)),
    "processor": (("microchip", 2), ("cable", 2), ("capacitor", 1)),
    "graphics card": (("casing", 1), ("microchip", 2), ("circuit board", 1)),
    "hard drive": (("casing", 1), ("circuit board", 1), ("cable", 2)),
    "solid state drive": (("casing", 1), ("circuit board", 1), ("microchip", 1)),
    "ram": (("microchip", 1), ("cable", 1), ("circuit board", 1))
}


def show_stats():
    out = ""

    for each in data["inventory"]:
        out += "%s: %d" % (each, data["inventory"][each])
        out += "\n"

    for each in data["computer"]:
        out += "%s added" % each if data["computer"][each] else "%s not yet added" % each
        out += "\n"

    return out


def load(id_num):
    # Check for file
    file_name = "saves/" + str(id_num) + ".json"
    if os.path.exists(file_name):
        # print("file %s.json exists" % str(id_num))
        data = {}
        with open(file_name, "r") as f:
           data = json.load(f)
        return data
    else:
        return copy.deepcopy(_frame)


def save(id_num, data):
    file_name = "saves/" + str(id_num) + ".json"
    with open(file_name, "w+") as f:
        json.dump(data, f)


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
        elif cmd[n] != args[n].lower():
            return False
        return True

    # If the command is not at least as long as the args, it is obviously False
    if len(cmd) < len(args):
        return False

    n = 0
    while n < len(args):
        if not arg_matches_cmd(n):
            return False
        n += 1

    return True


def has_all_ingredients(recipe):
    for mat in recipe:
        if data["inventory"][mat[0]] < mat[1]:
            return False

    for mat in recipe:
        data["inventory"][mat[0]] -= mat[1]

    return True


def craft():
    if len(cmd) == 1:
        out = "What would you like to craft?"
        return out

    # Component-related commands
    for each in _components:
        if check_cmd("craft", *each.split(" ")):
            if has_all_ingredients(component_recipes[each]):

                return "You craft a %s" % each
            else:
                return "You do not have all the required materials to craft a %s" % each
    if check_cmd("craft", ["component", "components"]):
        out = "**COMPONENT CRAFTING MENU**"
        # for each in component_recipes.items():
        #     print(each)
        #     to_print = each[0] + ":\n"
        #     for mat in each[1]:
        #         to_print += mat[0] + ": " + str(mat[1]) + ", "
        #     out += "\n" + to_print[:-2] + "\n"
        return out

    # Part-related commands
    for each in _parts:
        if check_cmd("craft", *each.split(" ")):
            return "You craft a %s" % each
    if check_cmd("craft", ["part", "parts"]):
        out = "**PART CRAFTING MENU**"
        # for each in part_recipes.items():
        #     print(each)
        #     to_print = each[0] + ":\n"
        #     for mat in each[1]:
        #         to_print += mat[0] + ": " + str(mat[1]) + ", "
        #     out += "\n" + to_print[:-2] + "\n"
        return out

    return "What would you like to craft?"


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


def process():
    out = ""
    for each in _materials:
        r = random.randint(0, 2)
        if r > 0:
            out += "You get %d %s\n" % (r, each)
            data["inventory"][each] += r

    return out


def run_command(id_num, cmd_string):
    global data
    data = load(id_num)
    print(data)

    global cmd
    cmd = cmd_string

    return_string = "You do nothing, probably because it hasn't been coded yet."

    if check_cmd("craft"):
        return_string = craft()
    elif check_cmd("stats"):
        return_string = show_stats()
    elif check_cmd("fix"):
        return_string = fix()
    elif check_cmd("process"):
        return_string = process()

    save(id_num, data)

    return return_string
