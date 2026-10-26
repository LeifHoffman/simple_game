'''
Basic RPG, Main file
Made by: Leif Hoffman
Start Date: 10/20/2026
'''

# Import neccessary modules/files
from characters import *
from add_functions import *
from story import *
from combat import *
from artifact_effects import *
import subprocess
import time
import sys
import json

# Clear terminal
subprocess.run("cls", shell=True, check=True)

# Initialize global variables
playerChoice = ""

# Load hero options
f = open("hero_info.json")
heroInfo = json.load(f)

heroChoices = []
for i in heroInfo:
    heroChoices.append(i)

# Prompt player selection
while playerChoice not in heroChoices:
    styleprint("Hero choices:")
    print("\n")
    for i in heroInfo:
        styleprint(i+":")
        print("")
        styleprint(f"Stats ---> HP: {heroInfo[i]['HP']} ATK: {heroInfo[i]['ATK']} DEF: {heroInfo[i]['DEF']} MG: {heroInfo[i]['MG']}")
        time.sleep(1)
        print("\n")

    styleprint("Enter which hero you would like to play: ")
    playerChoice = input().capitalize()
    if playerChoice not in heroChoices:
        styleprint("Invalid choice, please select again!")
        time.sleep(2)
        subprocess.run("cls", shell=True, check=True)
    else:
        while True:
            styleprint(f"You chose to play {playerChoice}. Are you sure (Y/N)? ")
            yn = input().upper()
            if yn == "Y":
                break
            elif yn == "N":
                playerChoice = ""
                break
            else:
                styleprint("Not a valid answer...")
        
# Set player stats
playerStats = Hero(name = playerChoice, hp = heroInfo[playerChoice]['HP'], maxHp = heroInfo[playerChoice]['HP'], damage = heroInfo[playerChoice]['ATK'], baseDamage=heroInfo[playerChoice]['ATK'], defense=heroInfo[playerChoice]['DEF'], baseDefense=heroInfo[playerChoice]['DEF'], baseMagic=heroInfo[playerChoice]['MG'], magic=heroInfo[playerChoice]['MG'])

# Opening story dialogue
storyStart()
subprocess.run("cls", shell=True, check=True)

# Test to see if artifact spawns work
spawnArtifact(playerStats, 0)

# Initiate Prologue Fight
startCombat(playerStats)
subprocess.run("cls", shell=True, check=True)

# Run infinite battle loop (Or don't, it's whatever you feel like)
while True:
    startCombat(playerStats)
    