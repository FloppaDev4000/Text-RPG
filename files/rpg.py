# text based game
# Author: Adam Noonan
# based on the game Mordhau, developed by Triternion

# ISSUES:
# kills amount doesn't update in "status" message.
# code is disgusting
# I don't know how this programme works
# need more comments
# unable to report maul man

# import nonsense
import random
from time import sleep
import csv

# TITLE SEQUENCE!
print(r"  __  __  ____  _____  _____  _    _         _    _ ")
print(r" |  \/  |/ __ \|     \|  __ \| |  | |   /\  | |  | |")
print(r" | \  / | |  | | |__) | |  | | |__| |  /  \ | |  | |")
print(r" | |\/| | |  | |  _  /| |  | |  __  | / /\ \| |  | |")
print(r" | |  | | |__| | | \ \| |__| | |  | |/ ____ \ |__| |")
print(r" |_|  |_|\____/|_|  \_\_____/|_|  |_/_/    \_\____/ ")
print(r"                                                    ")

name = input("What is your name? >> ")
print(f"\nOkay {name}, type \"help\" for a list of commands!")

# debug one second
one = 0.1

# get all the bad guys from the JSON ( or csv )
enemiesFilename = "enemies.csv"
with open(enemiesFilename, encoding="utf-8") as f:
    reader = csv.reader(f)
    enemies = list(reader)
    #data = json.load(f)
    #print(data)

# basic character class
class character:
    def __init__(self):
        self.bio = []
        self.hp = 1
            
# enemy character
class enemy(character):
    def __init__(self):
        character.__init__(self)
        self.bio = chooseOpponent()
        print(f"\nYou encounter a {self.bio[0]}! {self.bio[1]}")
        
# player character
class Player(character):
    fighting = False
    kills = 0
    def __init__(self):
        character.__init__(self)
        global you
        self.bio = you
        
    # regular actions
    def help(self): print(helpPrompt)
    def status(self):
        if self.hp > 0:
            print(aliveStatus, "Also, you have " + str(self.kills) + " kills.")
        else:
            print(deadStatus)
    def quit(self): quit()
    def move(self):
        if self.fighting == True:
            print("\nYou can't move forward right now! You're in battle, remember?")
            sleep(one)
        else:
            print("\nYou move onward...")
            sleep(one)
            self.enemy = enemy()
            self.fighting = True
            encounter(self, self.enemy)  
    
    # fight actions
    def surrender(self):
        self.act(0)
    def bomb(self):
        self.act(1)
    def arrow(self):
        self.act(2)
    def sword(self):
        self.act(3)
    def hammer(self):
        self.act(4)
    def report(self):
        self.act(5)
    
    def act(self, number):
        self.hp = fightResult(number, self)
        if self.hp > 0:
            print("\n" + self.bio[0], "killed", self.enemy.bio[0] + ".")
            self.fighting = False
            self.kills += 1

# big list of options and stuff
options = {"HELP": Player.help,
           "STATUS": Player.status,
           "QUIT": Player.quit,
           "MOVE FORWARD": Player.move}
optionsList = ("HELP",
           "STATUS",
           "QUIT",
           "MOVE FORWARD")

actions = {"SURRENDER": Player.surrender,
           "BOMB": Player.bomb,
           "ARROW": Player.arrow,
           "SWORD": Player.sword,
           "HAMMER": Player.hammer}
actionsList = ["SURRENDER",
           "BOMB",
           "ARROW",
           "SWORD",
           "HAMMER"]

# variables
you = [name,"It's you."]
p = Player()
helpPrompt = "\nAt any time you can use the following actions:\n" + ', '.join((optionsList)) + "\n\nIn battle, you can also use these actions:\n"+', '.join((actionsList))
aliveStatus = "\nWell, you're still alive so far. So that's pretty good."
deadStatus = "\nYou are dead, which is not very good."


# random opponent chooser
def chooseOpponent():
    global enemies
    try:
        opponent = random.choice(enemies)
        enemies.remove(opponent)
        return opponent
    except:
        print("\nThere are no opponents left. You have won!")
        sleep(one)
        quit()

# fight result calculator
def fightResult(type, player):
    type += 2
    interaction = player.enemy.bio[type]
    if interaction[0] == "-":
        health = 0
    else:
        health = 1
    interaction = (interaction[1:])
    print("\n" + interaction)
    sleep(one)
    return health

# begin the encounter
def encounter(p1, p2):
    sleep(one)
    print("\n" + p1.bio[0], "fights", p2.bio[0] + ".")

# loop runs all the time
while(p.hp > 0):
    action = input("\n>> ").upper()
    args = action.split()
    if len(args) > 0:
        optionFound = False
        if p.fighting:
            totalList = {**options,**actions}
        else:
            totalList = options
        for i in totalList.keys():
            if args[0] == i[:len(args[0])]:
                totalList[i](p)
                optionFound = True
                break
        if not optionFound:
            if args == "REPORTACCOUNT" or p.enemy.bio[0] == "naked maul man":
                p.report()
            else:
                print("\nNothing happened.")
        sleep(one)

# end of the game
if p.hp <= 0:
    sleep(one)
    print("\nYou Died! You got", p.kills, "kills.")