import random


class Die:
    """Represents a single die."""

    def __init__(self, sides=6):
        """Set the number of sides (defaults to six)."""
        self.sides = sides

    def roll(self):
        """Roll the die."""
        return random.randint(1, self.sides)


def roll3D6():
    roll1 = Die(6).roll()
    roll2 = Die(6).roll()
    roll3 = Die(6).roll()
    roll4 = Die(6).roll()
    minRoll = min(roll1, roll2, roll3, roll4)
    roll = roll1 + roll2 + roll3 + roll4 - minRoll
    return roll


class Item():
    """The base class for all items"""

    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)


class Gold(Item):

    def __init__(self, amt):
        self.amt = amt
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(
                             str(self.amt)),
                         value=self.amt)


class Character(object):
    """Represents any creatures"""

    def __init__(self, name, level, hp, maxhp, ac, inventory, exp,
                 strength, dex, con, wis, intel, cha):
        self.name = name
        self.level = level
        self.hp = hp
        self.maxhp = maxhp
        self.ac = ac
        self.inventory = inventory
        self.exp = exp
        self.strength = strength
        self.dex = dex
        self.con = con
        self.wis = wis
        self.intel = intel
        self.cha = cha


class Player(Character):
    """Represents a playable character"""

    def __init__(self, hp, maxhp):
        """Sets default stats for every playable class"""
        super().__init__(input("What is your characters name?\n>>>"),
                         1, hp, maxhp, 10,
                         {}, 0,
                         roll3D6(), roll3D6(), roll3D6(),
                         roll3D6(), roll3D6(), roll3D6())

    strength = roll3D6()
    dex = roll3D6()
    con = roll3D6()
    wis = roll3D6()
    intel = roll3D6()
    cha = roll3D6()
    PROFICIENCY = {1: 2, 2: 2, 3: 2, 4: 2,
                   5: 3, 6: 3, 7: 3, 8: 3,
                   9: 4, 10: 4, 11: 4, 12: 4,
                   13: 5, 14: 5, 15: 5, 16: 5,
                   17: 6, 17: 6, 18: 6, 19: 6, 20: 6}
    LEVEL2 = 300


class Fighter(Player):
    """Fighter class"""

    def __init__(self):
        super().__init__(hp=10, maxhp=10)

    PROF = "fighter"
    HD = 10
    ATTACKDIE = 10


class Cleric(Player):
    """Cleric class"""

    def __init__(self):
        super().__init__(hp=8, maxhp=8)

    PROF = "cleric"
    HD = 8
    ATTACKDIE = 6


class Mage(Player):
    """Mage class"""

    def __init__(self):
        super().__init__(hp=6, maxhp=6)

    PROF = "mage"
    HD = 6
    ATTACKDIE = 4


class Imp(Character):

    def __init__(self):
        super().__init__(name="imp",
                         hp=8, maxhp=8,
                         level=1,
                         ac=6, inventory={},
                         exp=200,
                         strength=6,
                         dex=17,
                         con=13,
                         wis=11,
                         intel=12,
                         cha=14)
    ATTACKDIE = 4


class Orc(Character):

    def __init__(self):
        super().__init__(name="orc",
                         hp=15, maxhp=15,
                         level=1,
                         ac=13,
                         inventory={},
                         exp=100,
                         strength=16,
                         dex=12,
                         con=16,
                         wis=7,
                         intel=11,
                         cha=10)
    ATTACKDIE = 12


class Young_Dragon(Character):

    def __init__(self):
        super().__init__(name="youngdragon",
                         hp=127, maxhp=127,
                         level=7,
                         ac=18,
                         inventory={},
                         exp=2900,
                         strength=19,
                         dex=14,
                         con=17,
                         wis=12,
                         intel=11,
                         cha=15)
    ATTACKDIE = 15


def playerAttack():
    roll = Die(20).roll()
    if roll == 20:
        rollD = Die(hero.ATTACKDIE).roll()
        rollD += Die(hero.ATTACKDIE).roll()
        print("You crit for", rollD, "damage")
        mob.hp -= rollD
        if mob.hp > 0:
            print("The", mob.name, "has", mob.hp, "hp left")
    elif roll == 1:
        print("You miss")
    elif roll + hero.PROFICIENCY[hero.level] >= mob.ac:
        rollD = Die(hero.ATTACKDIE).roll()
        print("You hit for", rollD, "damage")
        mob.hp -= rollD
        if mob.hp > 0:
            print("The", mob.name, "has", mob.hp, "hp left")
    else:
        print("You miss")


def monsterAttack():
    roll = Die(20).roll()
    if roll == 20:
        rollD = Die(mob.ATTACKDIE).roll() + 3
        rollD += Die(mob.ATTACKDIE).roll()
        print("The " + mob.name + " crits you for", rollD, "damage")
        hero.hp -= rollD
        print(hero.name, "has", hero.hp, "hp left")
    elif roll == 1:
        print("The " + mob.name + " misses you")
    elif roll >= hero.ac:
        rollD = Die(mob.ATTACKDIE).roll() + 3
        print("The " + mob.name + " hits you for", rollD, "damage")
        hero.hp -= rollD
        print(hero.name, "has", hero.hp, "hp left")
    else:
        print("The " + mob.name + " misses you")


def levelUp():
    """Checks to see if the hero has leveled up"""
    if hero.level == 20:
        print("You are at the level cap")
    else:
        while hero.exp >= hero.LEVEL2:
            hero.level += 1
            hero.maxhp += Die(hero.HD).roll()
            hero.hp = hero.maxhp
            if hero.PROF == "mage":
                hero.maxmana += 1
                hero.mana = hero.maxmana
            print("You Gained a level", "\n", 'hp:',
                  hero.maxhp, "\n", 'level:', hero.level)
            hero.exp -= hero.LEVEL2


def profession():
    letter_to_profession = {
        'f': Fighter,
        'c': Cleric,
        'm': Mage
    }
    print("What is your class?\n")
    for letter in letter_to_profession.keys():
        print("- Press {} for {}".format(
            letter, letter_to_profession[letter].__name__))
    pclass = input(">>>")
    return letter_to_profession[pclass]()


def encounter():
    letter_to_move = {
        'm': move,
        'r': rest
    }
    print("What would you like to do?\n")
    for letter in letter_to_move.keys():
        print("- Press {} for {}".format(
            letter, letter_to_move[letter].__name__))
    action = input(">>>")
    return letter_to_move[action]()


def move():
    if Die(100).roll() > 50:
        mob = ranmob()
        print("You see a ", mob.name)
        return mob
    else:
        hero.hp += 5
        if hero.hp > hero.maxhp:
            hero.hp = hero.maxhp
        print("You see nothing of interest and gain a little health. You are now on",
              hero.hp, "health")
        return None

def rest():
    hero.hp += 10
    if hero.hp > hero.maxhp:
        hero.hp = hero.maxhp
    print("You gain some health. You are now on", hero.hp, "health")
    return None


def ranmob():

    if hero.level < 5:
        mob = Imp() if Die(100).roll() > 10 else Orc()
    elif hero.level < 10:
        if Die(100).roll() > 60:
            mob = Imp()
        elif Die(100).roll() > 5:
            mob = Orc()
        else:
            mob = Young_Dragon()
    else:
        mob = Orc() if Die(100).roll() > 10 else Young_Dragon()
    return mob


def commands():
    if hero.PROF == "fighter":
        print(" -press f to fight", '\n',
              "-press enter to pass")
        command = input("~~~~~~~~~Press a key to Continue.~~~~~~~\n>>>")
        if command == "f":
            playerAttack()
        if command == "":
            pass

    if hero.PROF == "cleric":
        print(" -press f to fight", '\n',
              "-press h to heal", '\n',
              "-press enter to pass")
        command = input("~~~~~~~~~Press a key to Continue.~~~~~~~\n")
        if command == "f":
            playerAttack()
        elif command == "h":
            if hero.hp < hero.maxhp:
                hero.hp += Die(8).roll()
                if hero.hp > hero.maxhp:
                    hero.hp = hero.hp - (hero.hp - hero.maxhp)
                print("You now have:", hero.hp, "hp")
            else:
                print("Your hit points are full")
                commands()
        elif command == "":
            pass
    if hero.PROF == "mage":
        print("-press f to fight", '\n',
              "-press s for spells", '\n',
              "-press m to generate mana", '\n',
              "-press enter to pass")
        command = input("~~~~~~~~~Press a key to Continue.~~~~~~~\n")
        if command == "f":
            playerAttack()
        elif command == "s":
            print("You have", hero.mana, "mana")
            if hero.mana >= 1 and hero.mana < 3:
                print("press s for sleep", '\n',
                      "press m for magic missile")
                command = input(">>>")
                if command == "s":
                    print("You put the monster to sleep it is easy to kill now")
                    mob.hp -= mob.hp
                    hero.mana -= 1
                if command == "m":
                    if hero.mana < hero.maxmana:
                        hero.mana += Die(4).roll()
                        if hero.mana > hero.maxmana:
                            hero.mana -= (hero.mana - hero.maxmana)
                    dam = Die(4).roll() * hero.mana
                    mob.hp -= dam
                    print("You use all your mana! and do", dam, "damage!")
                    hero.mana -= hero.mana
            elif hero.mana >= 3:
                print("press s for sleep", '\n',
                      "press m for magic missile", '\n',
                      "press f for fireball")
                command = input(">>>")
                if command == "s":
                    print("You put the monster to sleep it is easy to kill now")
                    mob.hp -= mob.hp
                    hero.mana -= 1
                if command == "m":
                    dam = Die(4).roll() * hero.mana
                    mob.hp -= dam
                    print("You use all your mana! and do", dam, "damage!")
                    hero.mana -= hero.mana
                if command == "f":
                    print("You are temporarily blinded by a fiery flash of light.")
                    dam = 0
                    dam += Die(6).roll()
                    dam += Die(6).roll()
                    dam += Die(6).roll()
                    mob.hp -= dam
                    print("You did", dam, "points of damage")

                    hero.mana -= 3
            else:
                print("Your mana is empty")
                commands()
        elif command == "m":
            if hero.mana < hero.maxmana:
                hero.mana += 1
                print("You have", hero.mana, "mana")
            elif hero.mana >= hero.maxmana:
                print("Your mana is full.")
                print("You have", hero.mana, "mana")
                commands()

        elif command == "":
            pass


def generateHero():
    """Generate a hero (at start or upon a death)"""
    hero = profession()  # character creation point
    print("name hp ac inventory xp", '\n',
          hero.name, str(hero.hp) + "/" +
          str(hero.maxhp), hero.ac, hero.inventory, hero.exp,
          hero.strength, hero.dex, hero.con, hero.intel, hero.wis, hero.cha)
    return hero

hero = generateHero()
mob = encounter()

while True:
    if hero.hp <= 0:
        print(hero.name, "died!")
        print("You reached level", hero.level)
        hero = generateHero()
        mob = encounter()
    else:
        
    while mob != None and hero.hp > 0:
        print("You see", mob.name + ",", mob.name, "has", mob.hp, "hp.")
        if mob.hp <= 0:
            print('The', mob.name, 'is dead!')
            hero.exp += mob.exp
            print('Current exp:', hero.exp)
            levelUp()
            mob = encounter()
            print("mob.hp<=0")
        if hero.hp > 0:
            commands()
            print("hero.hp>0")
        if mob.hp > 0:
            monsterAttack()
            print("mob.hp>0")

    else:
        mob = encounter()

    """if mob != None:
        if mob.hp <= 0:
            print('The', mob.name, 'is dead!')
            hero.exp += mob.exp
            print('Current exp:', hero.exp)
            mob = ranmob()
        if hero.hp <= 0:
            print(hero.name, 'died!')
            #name=input("What is your characters name?")
            hero = generateHero()
            mob = ranmob()
        levelUp()

        print("You see", mob.name + ",", mob.name, "has", mob.hp, "hp.")
        if hero.hp > 0:
            commands()
        if mob.hp > 0:
            monsterAttack()"""
