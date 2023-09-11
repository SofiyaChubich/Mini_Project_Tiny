
import random
import json

def load_data(string):
    f = open(string)
    data = json.load(f)
    return data


def boss_fight():
    pass


def main_event(event):
    pass


def side_event():
    pass


def get_stats(string):
    data = load_data("backgr.json")[string]
    data["equipment"] = []
    return data

def update_stats():
    pass


character = get_stats(random.choice(["barbarian", "bard", "rogue"]))
main_q = load_data("main_scen.json")
for i in range(1, 4):
    main_event(main_q(str(i)))
    if i != 3:
        for _ in range(3):
            side_event()
    
 