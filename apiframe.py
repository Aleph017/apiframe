#!/usr/bin/env python3

import requests
import sys

colors = {
    "Grineer" : "\x1b[0;34;32m",
    "Corpus" : "\x1b[0;34;34m",
    "Infested" : "\x1b[0;34;31m",
    "clear" : "\x1b[0m"
}

def getFactionColor(faction):
    return colors.get(faction, colors["clear"])

print("Fetching data...", end="\r")

request = requests.get(f"https://api.warframestat.us/pc/")

if request.status_code != 200:
    print(f"Failed getting info from Warframe API: {request.status_code}", file=sys.stderr)
    exit()

response = request.json()

venusInfo = response["vallisCycle"]
cetusInfo = response["cetusCycle"]
deimosInfo = response["cambionCycle"]
duviriInfo = response["duviriCycle"]

baroInfo = response["voidTrader"]

invasions = response["invasions"]

print(f"Plains of Eidolon (Earth): {cetusInfo['state'].title()}, {cetusInfo['timeLeft']} left;")
print(f"Orb Vallis (Venus): {venusInfo['state'].title()}, {venusInfo['timeLeft']} left;")
print(f"Cambion Drift (Deimos): {deimosInfo['state'].title()}, {deimosInfo['timeLeft']} left;")
print(f"Duviri: {duviriInfo['state'].title()};\n")

if baroInfo["active"]:
    print(f"Void Trader: {baroInfo['location']}, {baroInfo['endString']} left;")
else:
    print(f"Void Trader: will be active in {baroInfo['startString']} at {baroInfo['location']};")

print("\nActive invasions:")

for invasion in invasions:
    if not invasion['completed']:
        node = invasion['nodeKey']
        attacker = invasion['attacker']['factionKey']
        defender = invasion['defender']['factionKey']
        eta = invasion['eta']
        defenderReward = invasion['defender']['reward']['asString']
        attackerColor = getFactionColor(attacker)
        defenderColor = getFactionColor(defender)
        if not invasion['vsInfestation']:
            attackReward = invasion['attacker']['reward']['asString']
            print(f"\t{node}:\n\t\t{attackerColor}{attacker}\x1b[0m ({attackReward}),\n\t\t{defenderColor}{defender}\x1b[0m ({defenderReward}),\n\t\t{eta} left;\n")
        else:
            print(f"\t{node}:\n\t\t{attackerColor}{attacker}\x1b[0m,\n\t\t{defenderColor}{defender}\x1b[0m ({defenderReward}),\n\t\t{eta} left;\n")
