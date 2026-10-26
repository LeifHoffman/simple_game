# Define base character class, includes HP, ATK, DEF
class Character:
    def __init__(self, name, hp=0, maxHp = 0, baseDamage=0, damage=0, nextDamage = 0, baseDefense=0, defense=0, nextDefense = 0, experience=0):
        self.name = name
        self.hp = hp
        self.maxHp = maxHp
        self.baseDamage = baseDamage
        self.damage = damage
        self.nextDamage = nextDamage
        self.baseDefense = baseDefense
        self.defense = defense
        self.nextDefense = nextDefense
        self.experience = experience

# Define enemy class
class Enemy(Character):
    def __init__(self, name, hp=0, maxHp = 0, baseDamage=0, damage=0, nextDamage = 0, baseDefense=0, defense=0, nextDefense = 0, experience=0):
        super().__init__(name, hp, maxHp, baseDamage, damage, nextDamage, baseDefense, defense, nextDefense, experience)

# Define hero class
class Hero(Character):
    def __init__(self, name, hp=0, maxHp = 0, baseDamage=0, damage=0, nextDamage = 0, baseDefense=0, defense=0, nextDefense = 0, experience=0, baseMagic=0, magic=0, artifacts=[]):
        super().__init__(name, hp, maxHp, baseDamage, damage, nextDamage, baseDefense, defense, nextDefense, experience)
        self.baseMagic = baseMagic
        self.magic = magic
        self.artifacts = artifacts

# Define artifacts class
class Artifact():
    def __init__(self, name, rarity, id, description):
        self.name = name
        self.rarity = rarity
        self.id = id
        self.description = description