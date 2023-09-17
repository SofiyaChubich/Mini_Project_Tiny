
import random
import json

#getting the appropriate data from the appropriate json files
def load_data(string):
    f = open(string)
    data = json.load(f)
    return data

#this is the code for when a boss fight happens
def boss_fight(boss):
    #I know this is technically bad, but there was too little time to do object oriented programming, so here we are
    global ch
    #this cycle will basically continue until either the player or the boss dies (reaches 0 HP)
    while boss["HP"] > 0 and ch["HP"] > 0:
        #this is just to make the output a little prettier
        print()
        #this is to inform the player how much HP they have left
        print("You have ", ch["HP"], " out of ", ch["Tot_HP"], "HP left.")
        choice = ""
        #this is where the player what the want to do, perform an attack, block and heal or do a special action
        while choice != "1" and choice != "2" and choice != "3":
            choice = input("1. Attack\n2. Guard\n3.Special skill\n(Please type in the number of your choice)\n")
        #if a player is poisoned they will take damage at the beginning of their turn
        if "poisoned" in ch["status"]:
            damage = roll_dice(1, 4)
            print("You suffer ", damage, " poison damage.")
        #if the player chose to attack this is where the "magic" happens
        if choice == "1":
            #we print out a pretty message to let the player know how their attack looks like
            print(ch["Attack_s"])
            #he we determine whether the player has advantage, disadvantage or if they just roll straight, depending on what effects are on them
            if ("charming" in ch["status"] or "hidden" in ch["status"]) and "frightened" not in ch["status"]:
                ch_roll = max(roll_dice(1, 20), roll_dice(1, 20))
            elif ("charming" not in  ch["status"] and  "hidden" not in ch["status"]) and "frightened" in ch["status"]:
                ch_roll = min(roll_dice(1, 20), roll_dice(1, 20))
            else:
                ch_roll = roll_dice(1, 20)
            #Here is where we add different modifiers to the attack roll for different classes
            if cl == "barbarian":
                ch_roll += ch["Strength"]
            else:
                ch_roll += ch["Dexterity"]
            #here we check if the player rolled high enough to break through the boss's armour class
            if ch_roll >= boss["AC"]:
                #if the player rolled well, we determine the damage and any additional bonuses to it
                damage = roll_dice(int(ch["Weapon"].split("d")[0]), int(ch["Weapon"].split("d")[1]))
                if "raging" in ch["status"]:
                    damage += 2
                if "hidden" in ch["status"]:
                    damage += roll_dice(1, 6)
                print("You deal ", damage, " points of damage.")
                boss["HP"] -= damage
            else:
                print("You deal no damage.")
            # if the player was "hidden" before the attack, they loose that status 
            if "hidden" in ch["status"]:
                ch["status"].remove("hidden")
        #if the player choice to a special skill - here is where we do it, the boss can still attack the player however
        elif choice == "3":
            special_skill(ch["Skill"])
        #if the player isn't guarding or hidden, the boss can attack
        if choice != "2" and "hidden" not in ch["status"]:
            print(boss["Attack_s"])
            #checking for advatage or disadvantage on the roll
            if "charming" in ch["status"]:
                boss_roll = min(roll_dice(1, 20), roll_dice(1, 20)) + boss["Modifier"]
            else:
                boss_roll = roll_dice(1, 20) + boss["Modifier"]
            chance = roll_dice(1, 2)
            #checking if the boss hits
            if boss_roll >= ch["AC"]:
                damage = roll_dice(int(boss["Weapon"].split("d")[0]), int(boss["Weapon"].split("d")[1]))
                #determining any damage bonuses or debuffs
                if "raging" in ch["status"]:
                    damage /= 2
                ch["HP"] -= damage
                print("You suffer ", damage, " points of damage.")
            else:
                print("It misses")
            #every turn a major boss has a 50/50 chance to use it's legendary skill
            if chance == 1 and "Legendary_sk" in boss.keys():
                print("Your opponent used ", boss["Legendary_sk"])
                special_skill(boss["Legendary_sk"])
        #if the player was raging and decided to guard, the rage dissapears
        if choice == "2" and "raging" in ch["status"]:
            ch["status"].remove("raging")
        # if the player chose to guard, they heal 2 HP, up to their Max HP
        if choice == "2":
            print("You heal two points of damage.")
            ch["HP"] += 2
            if ch["HP"] >= ch["Tot_HP"]:
                ch["HP"] = ch["Tot_HP"]
        
#This is a fubnction to run the main events
def main_event(event):
    print()
    print(event["Intro"])
    boss_fight(event)
    #checking if the player won or lost, and printing out the appropriate message
    if ch["HP"] <= 0:
        print(event["Outro L"])
    else:
        print(event["Outro W"])
    ch["status"] = []

#this is a function to run side events
def side_event(number_ev):
    #once again, I realise that doing global is not it in coding, but we do what we must
    #and yes, had there been more time, I would have done a bunch of classes and objects instead, but here we are
    global ch
    #loading in the appropriate event
    event = load_data("events.json")[number_ev]
    choice = ""
    print(event["Intro"])
    #choosing what the character should do, aka persuade, strength or dexterity
    while choice != "1" and choice != "2" and choice != "3":
        choice = input("1. Persuasion check\n2. Strength check\n3. Dexterity check\n(Please type in the number of your choice)")
    success = True
    # checking if the player succeeds on their roll for the appropriate skill
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
    #printing out appropriate message if they succeded
    if success:
        if choice == "1":
            print(event["P_S"])
        elif choice == "2":
            print(event["S_S"])
        elif choice == "3":
            print(event["D_S"])
    else:
        #and if the player rolled badly, they have to fight a mini boss (dw they are pretty easy)
        print(event["boss"]["Intro"])
        boss_fight(event["boss"])
        #printing out appropriate messages tambien
        if ch["HP"] <= 0:
            print(event["boss"]["Outro L"])
        else:
            print(event["boss"]["Outro W"])
    #if the player didn't duy the get Looy, yay
    if ch["HP"] > 0:
        print(event["Loot_text"])
        #if the player looted a weapon it's stats will just replace the character's ones
        #if it wasn't there will just be a bonus to their skills
        if event["Loot_type"] == "Weapon":
            ch[event["Loot_type"]] = event["Loot"]
            ch["Attack_s"] = event["Attack_s"]
        else:
            ch[event["Loot_type"]] += event["Loot"]
    

#here is where we get the character's "sheet"
def get_stats(cl):
    data = load_data("backgr.json")[cl]
    data["equipment"] = []
    data["status"] = []
    return data

#rolling the dice
def roll_dice(count, num):
    roll = 0
    for _ in range(count):
        roll += random.randint(1, num)
    return roll

#encating special skills
def special_skill(skill):
    global ch
    #loading loading loading
    skill = load_data("special_skills.json")[skill]
    chance = random.randint(1, 2)
    # if a "skill" is dependant there is a 50/50 chance it might not work
    #you may ask "Why did you put the boss's skill roll in the boss function and not just made it dependant?"
    #well, I didn't think that through enough, and here we are now
    if not skill["dependant"] or chance == 2:
        #checking if the skills deals any damage to the player
        if skill["damage"] != 0:
            damage = roll_dice(int(skill["damage"].split("d")[0]), int(skill["damage"].split("d")[1]))
            if "raging" in ch["status"]:
                damage /= 2
            ch["HP"] -= damage
            print("You suffer ", damage, " points of damage.")
        #checking if the skills adds any statuses to the plaer
        if skill["status"] != "None":
            ch["status"].append(skill["status"])
            print("You are", skill["status"], ".")




#randomising character's class
cl = random.choice(["barbarian", "bard", "rogue"])
ch = get_stats(cl)
#loading in the main boss fights
main_q = load_data("main_scen.json")
print("You wake up in what looks to be an abandoned wherehouse.\nYou don't remember who you are or where you came from.")
#every character gets their own intro, obviously
print(ch["Intro"])
#this is to help me randomise the order of the side events
list_ = ["1", "2", "3", "4", "5", "6"]
#cycling through the 3 main missions, aka bosses
for i in range(1, 4):
    if ch["HP"] <= 0:
        break
    #running the main event
    main_event(main_q[str(i)])
    if ch["HP"] <= 0:
        break
    #if the character survives, their HP gets restored and their statuses go away
    ch["HP"] = ch["Tot_HP"]
    print()

    #running the side events
    if i != 3:
        for _ in range(3):
            #randomising the order of side events
            ran = random.choice(list_)
            list_.remove(ran)
            side_event(ran) 
            if ch["HP"] <= 0:
                break
            #if the player is alive, we restore their health and get rid of any statuses
            ch["status"] = []
            ch["HP"] = ch["Tot_HP"]
            print()

#the winning message basically, ta-da
if ch["HP"] > 0:
    print("You continue wondering the wasteland.\nWho knows what adventures await you next.")