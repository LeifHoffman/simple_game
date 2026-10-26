'''
File for defining additonal functions
Made by: Leif Hoffman
Start: 10/20/2026
'''

from characters import Artifact
from artifact_effects import checkArtiPerms
import sys
import time
import json
import random
import subprocess

# Stylized Print Function
def styleprint(text):
    for let in text:
        sys.stdout.write(let)
        sys.stdout.flush()
        time.sleep(0.03)

# Niche function to handle checking existant names
def checkOptions(target, options):
    ls = []
    for item in options:
        ls.append(item.name)
    if target in ls:
        return False
    return True

# Spawn an artifact for the player to use
def spawnArtifact(player=0, luck=0, rewards=3):
    # Load artifact list
    f = open("artifact_info.json")
    artifacts = json.load(f)

    # Initialize choice list
    options = []

    # Get three random artifacts (Could be changed to have more options)
    for i in range(rewards):
        # Create artifact pool and rarity selection
        artifactPool = []
        rarity = ""

        # Change item pool based on luck
        itemLuck = luck * random.randrange(0, 100)
        if itemLuck < 40:
            rarity = "Common"
        elif itemLuck >= 40 and itemLuck < 70:
            rarity = "Uncommon"
        elif itemLuck >= 70 and itemLuck < 90:
            rarity = "Rare"
        else:
            rarity = "Legendary"

        # Put artifact names in item pool, all items must not already be in options
        # TODO? Prevent artifacts that player has from being added to the pool
        for item in artifacts[rarity]:
                if checkOptions(item, options):
                    newArtifact = Artifact(item, rarity, artifacts[rarity][item]["ID"], artifacts[rarity][item]["Description"])
                    artifactPool.append(newArtifact)

        options.append(artifactPool[random.randrange(0, len(artifactPool))])

    while True:
        styleprint("Choose an artifact to become stronger:")
        print("")
        for i in range(len(options)):
            styleprint(f"{i+1}: {options[i].name} ({options[i].rarity})")
            print("")
        styleprint("Option: ")
        select = int(input())
        if select not in [1, 2, 3]:
            styleprint("Not an option!")
            subprocess.run("cls", shell=True, check=True)
        else:
            player.artifacts.append(options[select-1])
            subprocess.run("cls", shell=True, check=True)
            if options[select-1].rarity == "Common":
                styleprint(f"You got the •{options[select-1].name}•!")
            if options[select-1].rarity == "Uncommon":
                styleprint(f"You got the ♦{options[select-1].name}♦!")
            if options[select-1].rarity == "Rare":
                styleprint(f"You got the ♥{options[select-1].name}♥!")
            if options[select-1].rarity == "Legendary":
                styleprint(f"You got the ∞{options[select-1].name}∞!")
            checkArtiPerms(player)
            time.sleep(2)
            return

