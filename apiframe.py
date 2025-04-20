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

def NGEcheck(string):
    return "Negative Time Error" if '-' in string else string

def requestInfo():
    request = requests.get("https://api.warframestat.us/pc/")
    if request.status_code != 200:
        print(f"Failed to get info from Warframestat API: {request.status_code}", 
              file=sys.stderr)
        sys.exit(1)
    return request.json()

def printCycles(response):
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

def printBaro(response):
    baroInfo = response["voidTrader"]
    if baroInfo["active"]:
        print(f"\nVoid Trader: {baroInfo['location']}, {NGEcheck(baroInfo['endString'])} left;")
    else:
        print(f"\nVoid Trader: will be active in {NGEcheck(baroInfo['startString'])} at {baroInfo['location']};")
    return None

def printInvasion(invasion, isColorful):
    if not invasion['completed']:
        node = invasion['nodeKey']
        attacker = invasion['attacker']['factionKey']
        defender = invasion['defender']['factionKey']
        attackReward = "" if invasion['vsInfestation'] else invasion['attacker']['reward']['asString']
        defenderReward = invasion['defender']['reward']['asString']
        attackerColor = "" if not isColorful else getFactionColor(attacker)
        defenderColor = "" if not isColorful else getFactionColor(defender)
        yellow = "" if not isColorful else "\x1b[0;34;33m"
        resetANSI = "" if not isColorful else "\x1b[0m"
        eta = NGEcheck(invasion['eta'])

        if not invasion['vsInfestation']:
            print(f"\t{node}:\n\t\t{attackerColor}{attacker}{resetANSI}:\n\t\t- Reward: {yellow}{attackReward}{resetANSI},\n\t\t{defenderColor}{defender}{resetANSI}:\n\t\t- Reward: {yellow}{defenderReward}{resetANSI},\n\t\t{eta} left;\n")
        else:
            print(f"\t{node}:\n\t\t{attackerColor}{attacker}{resetANSI},\n\t\t{defenderColor}{defender}{resetANSI}:\n\t\t- Reward: {yellow}{defenderReward}{resetANSI},\n\t\t{eta} left;\n")



def printInvasions(response, isColorful):
    invasions = response["invasions"]
    print("\nActive invasions:")
    for invasion in invasions:
        printInvasion(invasion, isColorful)
    
def printHelp():
    print("usage: apiframe [-c | --colorless] [-h | --help]\n\n-c | --colorless: disables colors in output\n-h | --help: prints this message\n")
    sys.exit(0)

def main(args):
    isColorful = True

    for arg in args:
        if arg == "-c" or arg == "--colorless":
            isColorful = False
        if arg == "-h" or arg == "--help":
            printHelp()

    response = requestInfo()
    printCycles(response)
    printBaro(response)
    printInvasions(response, isColorful)
    return 0

if __name__ == "__main__":
    main(sys.argv)
