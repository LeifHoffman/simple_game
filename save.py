'''
File to check and load saves
Made by: Leif Hoffman
Date: 10/26/2026
'''

from characters import *
from add_functions import styleprint
import json
import subprocess
import time

# Prompt which file to start on
def startFile():
    # Choose a save file to load
    while True:
        subprocess.run("cls", shell=True, check=True)
        styleprint("Select a save file to start:\n")
        for i in range(3):
            f = open(f"save{i+1}.json")
            save = ""
            try:
                save = json.load(f)
            except:
                pass
            if len(save) > 0:
                styleprint(f"{i+1}. {save["name"]}\n")
            else:
                styleprint(f"{i+1}. -----\n")
        styleprint("Option: ")
        choice = int(input())
        if choice in [1,2,3]:
            f = open(f"save{choice}.json")
            try:
                save = json.open(f)
            except:
                return choice
            # TODO THIS DOESN"T RUN!!! FIGURE OUT Y!
            styleprint("File already contains save data. Continue? (Y/N)\n")
            styleprint("Option: ")
            confirm = input().upper()
            if confirm not in ["Y", "N"]:
                styleprint("Invalid selection.")
            elif confirm == "Y":
                return choice
            time.sleep(1)
        else:
            styleprint("Invalid selection.")
            time.sleep(1)

# Prompt if player wants to load save data
def checkSave():
    while True:
        styleprint("Load save file? (Y/N)\n")
        styleprint("Option: ")
        choice = input().upper()
        if choice not in ["Y", "N"]:
            styleprint("Invalid answer!")
        elif choice == "N":
            return None
        else:
            subprocess.run("cls", shell=True, check=True)

            # Prompt save selection
            while True:
                subprocess.run("cls", shell=True, check=True)
                for i in range(3):
                    f = open(f"save{i+1}.json")
                    save = ""
                    try:
                        save = json.load(f)
                    except:
                        pass
                    if len(save) > 0:
                        styleprint(f"{i+1}. {save["name"]}\n")
                    else:
                        styleprint(f"{i+1}. -----\n")
                time.sleep(1)

# Save player data
def saveData(player, slot):
    # Prepare artifact save data
    artifactData = []
    for item in player.artifacts:
        artifactData.append([item.name, item.rarity, item.id, item.description])

    # Format save data
    data = {
        "name":player.name,
        "hp":player.hp,
        "maxHp":player.maxHp,
        "baseDamage":player.baseDamage,
        "damage":player.damage,
        "baseDefense":player.baseDefense,
        "defense":player.defense,
        "baseMagic":player.baseMagic,
        "magic":player.magic,
        "exp":player.experience,
        "artifacts":artifactData
    }

    # Save to the selected save slot
    with open(f"save{slot}.json","w") as out:
        json.dump(data, out)

# Test file saving/loading
if __name__ == "__main__":
    # Test slot selection
    slot = startFile()

    # Try saving to slot given a dummy character
    p = Hero("Knight", 10, 10, artifacts=[Artifact("Sword Pendant", "Common", 1, "Bleh")])
    saveData(p, slot)

    # Try loading save data
    h = checkSave()
    print(h)