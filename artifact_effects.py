'''
File for containing / handling artifact effects
Made by: Leif Hoffman
Date: 10/21/2026
'''

from characters import *

# Check to update player stats upon gaining an artifact i.e. permanent effects (Also can be used to reset stats =])
def checkArtiPerms(player):
    for arti in player.artifacts:
        match arti.id:
            case 1:
                player.damage = player.baseDamage + 1
            case 2:
                player.defense = player.baseDefense + 1
            case 3:
                player.magic = player.baseMagic + 1
            case 999:
                player.damage = player.baseDamage + 1
            case _:
                print("Item doesn't exist")

# Testing code
if __name__ == "__main__":
    p = Hero("Dummy", artifacts=[Artifact("Nord Hat", "Common", 999, "It's a hat, what do you think?")])
    checkArtiPerms(p)
    print("Dummy damage: ",p.damage)
    print("Dummy base damage: ",p.baseDamage)