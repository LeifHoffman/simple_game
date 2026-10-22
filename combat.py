'''
File for handling encounters
Made by: Leif Hoffman
Date: 10/20/2026
'''

from characters import *
from add_functions import *
import subprocess
import random
import json
import math


# Function for loading encounters, defaults to no rarity rng and one enemy
def loadEnemies(rng = 0, count = 1):
    # Load enemy list
    f = open("enemy_info.json")
    enemyInfo = json.load(f)
    enemyList = []

    for i in range(count):
        # Change encounter choices based on rng
        rarity = ""
        if rng == 0:
            rarity = "Common"
        # TODO Add in other encounter rarities / make rarity dynamic

        # Get enemy pool based on rarity
        enemyOption = []
        for name in enemyInfo[rarity]:
            enemyOption.append(name)
        #Assign random enemy from pool
        enemyID = enemyOption[random.randrange(0, len(enemyOption))]

        # Make enemy and add to list
        enemy = Enemy(enemyID, enemyInfo[rarity][enemyID]["HP"], enemyInfo[rarity][enemyID]["HP"], enemyInfo[rarity][enemyID]["ATK"], enemyInfo[rarity][enemyID]["ATK"], enemyInfo[rarity][enemyID]["DEF"], enemyInfo[rarity][enemyID]["DEF"])
        enemyList.append(enemy)

    return enemyList

# Function for handling damage
def dealDamage(target, attacker, modifier=1):
    init_damage = math.ceil(attacker.damage/modifier)
    # Ignore zero attack stat turns
    if init_damage == 0:
        styleprint(f"{attacker.name} couldn't deal damage!")
        print("")
    else:
        # Calculate damage
        incoming_damage = init_damage - target.defense
        # Make minimum damage 1 if the attacker has at least 1 ATK
        if incoming_damage <= 0:
            incoming_damage = 1
        target.hp -= incoming_damage
        styleprint(f"{attacker.name} dealt {incoming_damage} damage to {target.name}!")
        print("")
        if target.hp <= 0:
            styleprint(f"{target.name} was defeated!")
            print("")

# Check enemy status
def activeEnemies(enemies):
    for enemy in enemies:
        if enemy.hp > 0:
            return True
    return False

# Check if player is dead
def playerAlive(player):
    if player.hp > 0:
        return True
    return False

# Handle skill system
def skillList(player, enemies):
    # Show skill options based on class
    match player.name:
        case "Knight":
            styleprint("1. Spin Strike (physical)(all)")
            print("")
            styleprint("2. Muscle Up (self)")
            print("")
        case "Paladin":
            styleprint("1. Radiant Rain (magic)(all)")
            print("")
            styleprint("2. Holy Recovery (magic)(self)")
            print("")
        case "Wizard":
            styleprint("1. Fire Spark (magic)(single)")
            print("")
            styleprint("2. Electric Chain (magic)(all)")
            print("")
        case _:
            styleprint("1. NULL")
            print("")
    styleprint("Skill: ")
    choice = int(input())

    # Handle skill choice
    match choice:
        case 1:
            match player.name:
                case "Knight":
                    # Spin strike skill (attacks all enemies for player.damage/2 rounded up)
                    styleprint("You strike all enemies with your sword!")
                    print("")
                    time.sleep(1)
                    for target in enemies:
                        dealDamage(target, player, 2)
                        time.sleep(1)
                case "Paladin":
                    pass
                case "Wizard":
                    pass
            return True
        case 2:
            match player.name:
                case "Knight":
                    # Buff damage stat for remainder of the fight
                    styleprint("You brace yourself and prepare your muscles! ATK increased by 1 for this combat!")
                    print("")
                    player.damage += 1
                    time.sleep(1)
                case "Paladin":
                    pass
                case "Wizard":
                    pass
            return True

        # Handle default case for when improper action occurs
        case _:
            styleprint("Skill isn't available or doesn't exist!")
            return False

# Handle combat round
def combatRound(player, enemies):
    # Display living enemies
    styleprint("Enemies:")
    print("")
    for i in range(len(enemies)):
        if enemies[i].hp > 0:
            styleprint(f"{i+1}: {enemies[i].name} ")
            print("")
    print("")

    # Print player and their hp
    styleprint(f"---{player.name} HP: {player.hp}/{player.maxHp}")
    print("")

    # Prompt option
    styleprint("What would you like to do?")
    print("")
    styleprint("1. Attack")
    print("")
    styleprint("2. Skills")
    print("")
    styleprint("3. Check Enemy")
    print("")
    styleprint("4. Item")
    print("")
    styleprint("Action: ")
    choice = input()

    # Track if an action was successful
    actionSuccess = False
    # Handle attacking system
    if choice == "1":
        styleprint("Attack who?")
        print("")
        styleprint("Target: ")
        target = int(input())
        if target > len(enemies):
            styleprint("Enemy doesn't exist!")
        elif enemies[target-1].hp <= 0:
            styleprint("Enemy is already defeated!")
        else:
            dealDamage(enemies[target-1], player)
            actionSuccess = True
            time.sleep(2)
    # TODO Add magic/skill system per character
    if choice == "2":
        styleprint("What skill do you want to use?")
        print("")
        # Run skillList()
        actionSuccess = skillList(player, enemies)
    # Handle checking system
    if choice == "3":
            styleprint("Check who?")
            print("")
            styleprint("Target: ")
            target = int(input())
            if target > len(enemies):
                styleprint("Enemy doesn't exist!")
            elif enemies[target-1].hp <= 0:
                styleprint("Enemy is already defeated!")
            else:
                styleprint(f"Enemy Name: {enemies[target-1].name}")
                print("")
                styleprint(f"HP: {enemies[target-1].hp}/{enemies[target-1].maxHp}")
                print("")
                styleprint(f"Damage: {enemies[target-1].damage}")
                print("")
                styleprint(f"Defense: {enemies[target-1].defense}")
                print("")
                styleprint("Enter to continue...")
                input()
                actionSuccess = True
    # TODO Add item iteraction
    if choice == "4":
        pass
    # Pause temporarily to infom player on action failure
    if actionSuccess == False:
        time.sleep(2)
    # End combat if all enemies are defeated
    elif activeEnemies(enemies) == False:
        return
    # Handle enemy turn afterwards if any are alive
    else:
        styleprint("Enemies attack!")
        print("")
        for enemy in enemies:
            if enemy.hp > 0:
                dealDamage(player, enemy)
                time.sleep(1)
            if playerAlive(player) == False:
                return

# Test/Prologue Combat
def startPrologueCombat(player):
    # Alert player of enemy
    subprocess.run("cls", shell=True, check=True)
    styleprint("An enemy approaches!")
    time.sleep(2)
    subprocess.run("cls", shell=True, check=True)

    # Create one enemy
    enemies = loadEnemies()
    while True:
        combatRound(player, enemies)
        if activeEnemies(enemies) == False:
            styleprint("All enemies are defeated!")
            time.sleep(2)
            break
        if playerAlive(player) == False:
            styleprint(f"{player.name} was defeated...")
            time.sleep(2)
            break
        subprocess.run("cls", shell=True, check=True)

# Regular Combat
def startCombat(player):
    # Alert player of enemy
    subprocess.run("cls", shell=True, check=True)
    styleprint("An enemy approaches!")
    time.sleep(2)
    subprocess.run("cls", shell=True, check=True)

    # Create enemies
    enemies = loadEnemies(0, random.randrange(1,3))
    while True:
        combatRound(player, enemies)
        if activeEnemies(enemies) == False:
            styleprint("All enemies are defeated!")
            time.sleep(2)
            break
        if playerAlive(player) == False:
            styleprint(f"{player.name} was defeated...")
            time.sleep(2)
            break
        subprocess.run("cls", shell=True, check=True)

# Test Combat
if __name__ == "__main__":
    p = Hero("Dummy", 10, 10, 1, 1, 1, 1, 0, 1, 1)
    e = []
    for i in range(3):
        e.append(Enemy("Dummy", 999, 999, 0, 0, 0, 0, 0))
    while True:
        combatRound(p, e)
        if activeEnemies(e) == False:
            styleprint("All enemies are defeated!")
            time.sleep(2)
            break
        if playerAlive(p) == False:
            styleprint(f"{p.name} was defeated...")
            time.sleep(2)
            break
        subprocess.run("cls", shell=True, check=True)