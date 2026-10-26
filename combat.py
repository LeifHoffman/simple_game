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
    init_damage = math.ceil((attacker.damage + attacker.nextDamage)*modifier)
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

# Function for handling healing
def recoverHealth(target, amount, percentage):
    heal = amount
    # Heal by target HP percent (round up) if percentage is true
    if percentage == True:
        heal = math.ceil(target.maxHp * amount/100)
        target.hp += heal
    # Heal by amount otherwise
    else:
        target.hp += heal

    # Report heal amount if not full. If full or higher, set to max
    if target.hp >= target.maxHp:
        target.hp == target.maxHp
        styleprint(f"{target.name} was fully healed!")
    else:
        styleprint(f"{target.name} was healed for {heal} HP!")
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
                        dealDamage(target, player, 1/2)
                        time.sleep(1)
                    player.nextDamage = 0
                case "Paladin":
                    # Radiant rain skill (attack all enemies for player.damage*2, uses MG)
                    if player.magic > 0:
                        styleprint("With a prayer, light sunders your enemies!")
                        print("")
                        for target in enemies:
                            dealDamage(target, player, 2)
                            time.sleep(1)
                        player.magic -= 1
                    else:
                        styleprint("Not enough MG!")
                        return False
                case "Wizard":
                    # Fire spark skill (attack one enemy for player.damage * 4, uses MG)
                    if player.magic > 0:
                        styleprint("Fire spark on who?")
                        print("")
                        styleprint("Target: ")
                        target = int(input())
                        if target > len(enemies):
                            styleprint("Enemy doesn't exist!")
                            return False
                        elif enemies[target-1].hp <= 0:
                            styleprint("Enemy is already defeated!")
                            return False
                        else:
                            styleprint(f"You let loose a flame on {enemies[target-1].name}!")
                            print("")
                            time.sleep(1)
                            dealDamage(enemies[target-1], player, 4)
                            player.magic -= 1
                        time.sleep(1)
                    else:
                        styleprint("Not enough MG!")
                        return False
            return True
        case 2:
            match player.name:
                case "Knight":
                    # Buff damage stat for remainder of the fight
                    styleprint("You brace yourself and prepare your muscles! ATK increased by 1 for next attack!")
                    print("")
                    player.nextDamage += 1
                    time.sleep(1)
                case "Paladin":
                    # Holy recovery skill (heal equal to 20% HP, uses MG)
                    if player.magic > 0:
                        styleprint("You held your symbol aloft, and felt your wounds heal!")
                        print("")
                        recoverHealth(player, 20, True)
                        player.magic -= 1
                    else:
                        styleprint("Not enough MG!")
                        return False
                case "Wizard":
                    # Electric chain skill (attack all enemies for player.damage * 3, uses MG)
                    if player.magic > 0:
                        styleprint("Electricity bolts between your enemies!")
                        print("")
                        for target in enemies:
                            dealDamage(target, player, 3)
                            time.sleep(1)
                        player.magic -= 1
                    else:
                        styleprint("Not enough MG!")
                        return False
            return True

        # Handle default case for when improper action occurs
        case _:
            styleprint("Skill isn't available or doesn't exist!")
            return False

# Handle combat round
def combatRound(player, enemies, turnCount):
    # Display round number
    styleprint(f"Round #{turnCount}")
    print("\n")
    # Display living enemies
    styleprint("Enemies:")
    print("")
    for i in range(len(enemies)):
        if enemies[i].hp > 0:
            styleprint(f"{i+1}: {enemies[i].name} ")
            print("")
    print("")

    # Print player and their hp + mg
    styleprint(f"---{player.name} HP: {player.hp}/{player.maxHp} MG: {player.magic}")
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
            player.nextDamage = 0
    # Handle magic/skill system
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
        time.sleep(1)
        for enemy in enemies:
            if enemy.hp > 0:
                dealDamage(player, enemy)
                time.sleep(1)
            if playerAlive(player) == False:
                return

# Regular Combat
def startCombat(player):
    # Alert player of enemy
    subprocess.run("cls", shell=True, check=True)
    styleprint("An enemy approaches!")
    time.sleep(2)
    subprocess.run("cls", shell=True, check=True)

    # Create turn counter
    turn = 0
    # Create enemies
    enemies = loadEnemies(0, random.randrange(1,3))
    while True:
        turn += 1
        combatRound(player, enemies, turn)
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
    styleprint("Enter test hero name:")
    name = (input()).capitalize()
    p = Hero(name = name, hp = 10, maxHp=10, damage=1, defense=1, baseDamage=1, baseDefense=1, experience=0, baseMagic=1, magic=1)
    e = []
    t = 0
    for i in range(3):
        e.append(Enemy("Dummy", 999, 999, 0, 0, 0, 0, 0))
    while True:
        subprocess.run("cls", shell=True, check=True)
        t += 1
        combatRound(p, e, t)
        if activeEnemies(e) == False:
            styleprint("All enemies are defeated!")
            time.sleep(2)
            break
        if playerAlive(p) == False:
            styleprint(f"{p.name} was defeated...")
            time.sleep(2)
            break
        subprocess.run("cls", shell=True, check=True)