
import random
import json

def load_data(string):
    f = open(string)
    data = json.load(f)
    return data


def boss_fight(boss):
    global ch

    while boss["HP"] > 0 and ch["HP"] > 0:
        ch_roll = roll_dice(1, 20)
        if cl == "barbarian":
            ch_roll += ch["Strength"]
        else:
            ch_roll += ch["Dexterity"]

        if ch_roll >= boss["AC"]:
            boss["HP"] -= roll_dice(ch["Weapon"].split("d")[0], ch["Weapon"].split("d")[1])

        boss_roll = roll_dice(1, 20) + boss["modifier"]
        chance = roll_dice(1, 2)
        if boss_roll >= ch["AC"]:
            ch["HP"] -= roll_dice(boss["Weapon"].split("d")[0], boss["Weapon"].split("d")[1])

        if chance == 1:
            special_skill(boss["legendary_sk"])



def main_event(event):
    boss_fight(event)
    if ch["HP"] <= 0:
        pass
    else:
        pass


def side_event():
    pass

def get_stats(string):
    data = load_data("backgr.json")[string]
    data["equipment"] = []
    data["status"] = []
    return data

def update_stats():
    pass

def roll_dice(count, num):
    roll = 0
    for _ in range(count):
        roll += random.randint(1, num)
    return roll

def special_skill(skill):
    global ch
    dict_ = load_data("special_skills.json")[skill]
    if skill["damage"] != 0:
        ch["HP"] -= roll_dice(skill["damage"].split("d")[0], skill["damage"].split("d")[1])
    if skill["status"] != "None":
        ch["status"].append(skill["status"])





cl = random.choice(["barbarian", "bard", "rogue"])
ch = get_stats("backgr.json")[cl]
main_q = load_data("main_scen.json")
for i in range(1, 4):
    main_event(main_q[str(i)])
    if i != 3:
        for _ in range(3):
            side_event() 