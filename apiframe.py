#!/usr/bin/env python3

import requests
import sys

colors = {
    "Grineer" : "\x1b[0;34;32m",
    "Corpus" : "\x1b[0;34;34m",
    "Infested" : "\x1b[0;34;31m",
    "clear" : "\x1b[0m"
}

yellow = "\x1b[0;34;33m"

def getFactionColor(faction):
    return colors.get(faction, colors["clear"])

print("Fetching data...", end="\r")

request = requests.get(f"https://api.warframestat.us/pc/")

if request.status_code != 200:
    print(f"Failed getting info from Warframestat API: {request.status_code}", file=sys.stderr)
    sys.exit(1)

response = request.json()

cycles = {
    "venusInfo" : {
        "info" : response["vallisCycle"],
        "name" : "Orb Vallis (Venus)"
    },
    "cetusInfo" : {
        "info" : response["cetusCycle"],
        "name" : "Plains of Eidolon (Earth)"
    },
    "deimosInfo" : {
        "info" : response["cambionCycle"],
        "name" : "Cambion Drift (Deimos)"
    },
    "duviriInfo" : {
        "info" : response["duviriCycle"],
        "name" : "Duviri"
    }
}

baroInfo = response["voidTrader"]

invasions = response["invasions"]

for key, cycle in cycles.items():
    if cycle['name'] != "Duviri":
        eta = ""
        if cycle['name'] != "Duviri" and '-' in cycle['info']['timeLeft']:
            eta = "Negative Time Error"
        else:
            eta = cycle['info']['timeLeft']
        print(f"{cycle['name']}: {cycle['info']['state'].title()}, {eta} left;") 
    else:
        print(f"{cycle['name']}: {cycle['info']['state'].title()};")
    
if baroInfo["active"]:
    print(f"\nVoid Trader: {baroInfo['location']}, {baroInfo['endString']} left;")
else:
    print(f"\nVoid Trader: will be active in {baroInfo['startString']} at {baroInfo['location']};")

print("\nActive invasions:")

for invasion in invasions:
    if not invasion['completed']:
        node = invasion['nodeKey']
        attacker = invasion['attacker']['factionKey']
        defender = invasion['defender']['factionKey']
        eta = "Negative Time Error" if '-' in invasion['eta'] else invasion['eta']
        defenderReward = invasion['defender']['reward']['asString']
        attackerColor = getFactionColor(attacker)
        defenderColor = getFactionColor(defender)
        
        if not invasion['vsInfestation']:
            attackReward = invasion['attacker']['reward']['asString']
            print(f"\t{node}:\n\t\t{attackerColor}{attacker}\x1b[0m:\n\t\t- Reward: {yellow}{attackReward}\x1b[0m,\n\t\t{defenderColor}{defender}\x1b[0m:\n\t\t- Reward: {yellow}{defenderReward}\x1b[0m,\n\t\t{eta} left;\n")
        else:
            print(f"\t{node}:\n\t\t{attackerColor}{attacker}\x1b[0m,\n\t\t{defenderColor}{defender}\x1b[0m:\n\t\t- Reward: {yellow}{defenderReward}\x1b[0m,\n\t\t{eta} left;\n")
