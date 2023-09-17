
import random
import json

def load_data(string):
    f = open(string)
    data = json.load(f)
    return data


def boss_fight(boss):
    global ch
    while boss["HP"] > 0 and ch["HP"] > 0:
        print()
        print("You have ", ch["HP"], " out of ", ch["Tot_HP"], "HP left.")
        choice = ""
        while choice != "1" and choice != "2" and choice != "3":
            choice = input("1. Attack\n2. Guard\n3.Special skill\n(Please type in the number of your choice)\n")
        if "poisoned" in ch["status"]:
            damage = roll_dice(1, 4)
            print("You suffer ", damage, " poison damage.")
        if choice == "1":
            print(ch["Attack_s"])
            if ("charming" in ch["status"] or "hidden" in ch["status"]) and "frightened" not in ch["status"]:
                ch_roll = max(roll_dice(1, 20), roll_dice(1, 20))
            elif ("charming" not in  ch["status"] and  "hidden" not in ch["status"]) and "frightened" in ch["status"]:
                ch_roll = min(roll_dice(1, 20), roll_dice(1, 20))
            else:
                ch_roll = roll_dice(1, 20)
            if cl == "barbarian":
                ch_roll += ch["Strength"]
            else:
                ch_roll += ch["Dexterity"]

            if ch_roll >= boss["AC"]:
                damage = roll_dice(int(ch["Weapon"].split("d")[0]), int(ch["Weapon"].split("d")[1]))
                if "raging" in ch["status"]:
                    damage += 2
                if "hidden" in ch["status"]:
                    damage += roll_dice(1, 6)
                print("You deal ", damage, " points of damage.")
                boss["HP"] -= damage
            else:
                print("You deal no damage.")
            if "hidden" in ch["status"]:
                ch["status"].remove("hidden")
        elif choice == "3":
            special_skill(ch["Skill"])
        if choice != "2" and "hidden" not in ch["status"]:
            print(boss["Attack_s"])
            if "charming" in ch["status"]:
                boss_roll = min(roll_dice(1, 20), roll_dice(1, 20)) + boss["Modifier"]
            else:
                boss_roll = roll_dice(1, 20) + boss["Modifier"]
            chance = roll_dice(1, 2)
            if boss_roll >= ch["AC"]:
                damage = roll_dice(int(boss["Weapon"].split("d")[0]), int(boss["Weapon"].split("d")[1]))
                if "raging" in ch["status"]:
                    damage /= 2
                ch["HP"] -= damage
                print("You suffer ", damage, " points of damage.")
            else:
                print("It misses")

            if chance == 1 and "Legendary_sk" in boss.keys():
                print("Your opponent used ", boss["Legendary_sk"])
                special_skill(boss["Legendary_sk"])
        if choice == "2" and "raging" in ch["status"]:
            ch["status"].remove("raging")
        if choice == "2":
            print("You heal two points of damage.")
            ch["HP"] += 2
            if ch["HP"] >= ch["Tot_HP"]:
                ch["HP"] = ch["Tot_HP"]
        

def main_event(event):
    print()
    print(event["Intro"])
    boss_fight(event)
    if ch["HP"] <= 0:
        print(event["Outro L"])
    else:
        print(event["Outro W"])
    ch["status"] = []


def side_event(number_ev):
    global ch
    event = load_data("events.json")[number_ev]
    choice = ""
    print(event["Intro"])
    while choice != "1" and choice != "2" and choice != "3":
        choice = input("1. Persuasion check\n2. Strength check\n3. Dexterity check\n(Please type in the number of your choice)")
    success = True
    if choice == "1":
        roll = roll_dice(1, 20) + ch["Persuasion"]
        if roll < event["P_AC"]:
            success = False
    elif choice == "2":
        roll = roll_dice(1, 20) + ch["Strength"]
        if roll < event["S_AC"]:
            success = False
    elif choice == "3":
        roll = roll_dice(1, 20) + ch["Dexterity"]
        if roll < event["D_AC"]:
            success = False

    if success:
        if choice == "1":
            print(event["P_S"])
        elif choice == "2":
            print(event["S_S"])
        elif choice == "3":
            print(event["D_S"])
    else:
        print(event["boss"]["Intro"])
        boss_fight(event["boss"])
        if ch["HP"] <= 0:
            print(event["boss"]["Outro L"])
        else:
            print(event["boss"]["Outro W"])

    if ch["HP"] > 0:
        print(event["Loot_text"])
        if event["Loot_type"] == "Weapon":
            ch[event["Loot_type"]] = event["Loot"]
            ch["Attack_s"] = event["Attack_s"]
        else:
            ch[event["Loot_type"]] += event["Loot"]
    


def get_stats(cl):
    data = load_data("backgr.json")[cl]
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
    skill = load_data("special_skills.json")[skill]
    chance = random.randint(1, 2)
    if not skill["dependant"] or chance == 2:
        if skill["damage"] != 0:
            damage = roll_dice(int(skill["damage"].split("d")[0]), int(skill["damage"].split("d")[1]))
            if "raging" in ch["status"]:
                damage /= 2
            ch["HP"] -= damage
            print("You suffer ", damage, " points of damage.")
        if skill["status"] != "None":
            ch["status"].append(skill["status"])
            print("You are", skill["status"], ".")





cl = random.choice(["barbarian", "bard", "rogue"])
ch = get_stats(cl)
main_q = load_data("main_scen.json")
print("You wake up in what looks to be an abandoned wherehouse.\nYou don't remember who you are or where you came from.")
print(ch["Intro"])
list_ = ["1", "2", "3", "4", "5", "6"]
for i in range(1, 4):
    if ch["HP"] <= 0:
        break
    main_event(main_q[str(i)])
    if ch["HP"] <= 0:
        break
    ch["HP"] = ch["Tot_HP"]
    print()

    if i != 3:
        for _ in range(3):
            ran = random.choice(list_)
            list_.remove(ran)
            side_event(ran) 
            if ch["HP"] <= 0:
                break
            ch["status"] = []
            ch["HP"] = ch["Tot_HP"]
            print()

if ch["HP"] > 0:
    print("You continue wondering the wasteland.\nWho knows what adventures await you next.")