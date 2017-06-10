import textwrap as txt
import shutil
import time as ti
import os
import rooms

from imp import reload
from objects import Item, Container, TransportProp

CONSOLEWIDTH = shutil.get_terminal_size(0)[0]

TITLE = [
	"{:^{w}}".format("###########################################################################################", w=CONSOLEWIDTH),
	"{:^{w}}".format("#  _____       _ _ _       _       _____      _  __  ______          _             _ _    #", w=CONSOLEWIDTH),
	"{:^{w}}".format("# /  __ \     | | (_)     ( )     /  ___|    | |/ _| | ___ \        | |           (_) |   #", w=CONSOLEWIDTH),
	"{:^{w}}".format("# | /  \/ ___ | | |_ _ __ |/ ___  \ `--.  ___| | |_  | |_/ /__  _ __| |_ _ __ __ _ _| |_  #", w=CONSOLEWIDTH),
	"{:^{w}}".format("# | |    / _ \| | | | '_ \  / __|  `--. \/ _ \ |  _| |  __/ _ \| '__| __| '__/ _` | | __| #", w=CONSOLEWIDTH),
	"{:^{w}}".format("# | \__/\ (_) | | | | | | | \__ \ /\__/ /  __/ | |   | | | (_) | |  | |_| | | (_| | | |_  #", w=CONSOLEWIDTH),
	"{:^{w}}".format("#  \____/\___/|_|_|_|_| |_| |___/ \____/ \___|_|_|   \_|  \___/|_|   \__|_|  \__,_|_|\__| #", w=CONSOLEWIDTH),
	"{:^{w}}".format("#                                                                                         #", w=CONSOLEWIDTH),
	"{:^{w}}".format("###########################################################################################", w=CONSOLEWIDTH),
]	
		
COMMANDS_HELP = [
	"attack   <target>  (with <item>)  - Attack or attempt to break something",
	"drop   <item>  - Drop an item from you inventory",
	"go   <direction>  - Travel north/south/east/west",
	"hold   <item>  - Equips or de-equips an item (used for default attack)",
	"inventory  - See what items you have acquired",
	"look  (<target>)  - Look around the room or take a closer look at something",
	"quit  - Restart the game",
	"take   <target>  - Pick up an item to put in your inventory",
	"use   <item>  (on <target>)  - Interact with an object or use an item from your inventory",
]

CHECK_DIRECTION = {
	"north": "north",
	"forward": "north",
	"forwards": "north",
	"n": "north",
	"south": "south",
	"backward": "south",
	"backwards": "south",
	"s": "south",
	"east": "east",
	"right": "east",
	"e": "east",
	"west": "west",
	"left": "west",
	"w": "west"
}

txtWrap = txt.TextWrapper(CONSOLEWIDTH-2, initial_indent="  ", subsequent_indent="  ", replace_whitespace=False)
def Say(text):
	text = txtWrap.fill(text)
		
	print(text)
		
while(True):
	os.system('cls||clear')
	reload(rooms)
	from rooms import RemoveItem, AddItem, UpdateDescription, GetRoomAttribute, SetRoomAttribute
	
	class Player(object):
		exit = False
		holding = ""
		inventory = {}
		location = "Forest Clearing"
		name = ""

		def Attack(self, target, objects, objectUsed="unarmedAttack"):
			if((target in objects) and (isinstance(objects[target], Container))):
				if(objects[target].CheckIfOpened(objectUsed)):
					self.Use(target, objects, objectUsed)
					
				else:
					Say(objects[target].breakDescription)
			
			else:
				if(objectUsed != "unarmedAttack"):
					if(objectUsed in objects):
						breakText = ("")
						objectUsedStrength = objects[objectUsed].breakStrength
						
					else:
						breakText = ("You take out the %s and attack:" %objectUsed)
						objectUsedStrength = self.inventory[objectUsed].breakStrength
						
				else:
					if(self.holding != ""):
						breakText = ("You attack with the %s:" %self.holding)
						objectUsedStrength = self.inventory[self.holding].breakStrength
					
					else:
						breakText = ("")
						objectUsedStrength = 1
				
				if(target in objects):
					target = objects[target]
				
				else:
					target = self.inventory[target]
				
				if(objectUsedStrength > target.breakStrength):
					if(target.name in objects):
						Say("%s %s" %(breakText, target.breakDescription))
						RemoveItem(self.location, target.name)
						
					else:
						Say("%s %s" %(breakText, target.breakDescription))
						del self.inventory[target.name]
				
				elif(target.breakStrength == 5):
					Say("%s %s" %(breakText, target.breakDescription))
				
				else:
					Say("%s Nothing happens." %breakText)
			
		def Drop(self, target, objects):
			if(target in self.inventory):
				Say("You take out the %s and drop it on the ground." %target)
				AddItem(self.location, self.inventory[target])
				del self.inventory[target]
				
				if(self.holding == target):
					self.holding = ""
				
			else:
				Say("The %s is already on the ground." %target)

		def Go(self, target, objects):
			if(target in CHECK_DIRECTION):
				targetLocation = GetRoomAttribute(self.location, target)
				
				if(GetRoomAttribute(targetLocation, "isRoom")):
					objects = GetRoomAttribute(targetLocation, "objects")
				
				else:
					objects = {}
			
				if(GetRoomAttribute(targetLocation, "initial")):
					Say(GetRoomAttribute(targetLocation, "description_Initial"))
					UpdateDescription(targetLocation)
					
				else:
					baseText = GetRoomAttribute(targetLocation, "description_Default")
					objectText = []
					
					for object in objects.values():
						if(isinstance(object, Item)):
							objectText.append(object.info_setting)
						
					text = baseText + "".join(objectText)
						
					Say(text)
				
				if(GetRoomAttribute(targetLocation, "isRoom") is True):
					self.location = targetLocation
			
			else:
				Say("You must specify a direction to go, not an object.")

		def Help(self):
			newLines = []
		
			for line in COMMANDS_HELP:
				phrases = line.split("  ")
				if(len(phrases) == 2):
					newLines.append("  " + "{0:11}{1:14}{2:16}{3:60}".format(phrases[0],"","",phrases[1]))
				
				elif(len(phrases) == 3):
					newLines.append("  " + "{0:11}{1:14}{2:16}{3:60}".format(phrases[0],phrases[1],"",phrases[2]))
				
				elif(len(phrases) == 4):
					newLines.append("  " + "{0:11}{1:14}{2:16}{3:60}".format(phrases[0],phrases[1],phrases[2],phrases[3]))
			
			print("\n".join(newLines))

		def Hold(self, target, objects):
			if(target == self.holding):
				Say("You put away the %s." %target)
				self.holding = ""
			
			elif(target in self.inventory):	
				if(self.holding != ""):
					Say("You put away your %s and take out your %s." %(self.holding, target))
				
				else:
					Say("You take out your %s." %target)
			
				self.holding = target
			
		def Inventory(self):
			if(len(self.inventory) > 0):
				itemList = ", a ".join(self.inventory.keys())
				
				Say("You empty the contents of your backpack. You have collected: a %s" %itemList)
				
			else:
				Say("Your backpack is pretty light, not especially surprising since it's empty.")

		def Look(self, target="", objects=""):
			if(target != ""):
				if(target in objects):
					Say(objects[target].info_look)
				
				elif(self.holding == target):
					Say("You look at the %s in your hand: %s" %(target, self.inventory[target].info_look))
						
				else:
					Say("You take out the %s and look at it: %s" %(target, self.inventory[target].info_look))
					
			else:
				objects = GetRoomAttribute(self.location, "objects")
				Say("You look around and you see: a " + (", a ".join(list(objects.keys()))))

		def Quit(self):
			verify = input("Adventuring is busy work...Should I just abandon all hope now?\n  >> ").lower()
			
			if(verify == "y" or verify == "yes"):
				print("\nweaksauce.")
				ti.sleep(5)
				self.exit = True
				reload(rooms)
				
			else:
				print()
				Say("Shia Labeouf whispers in your ear, 'just do it %s.' Your resolve has been strengthened: you will not let your dreams be memes. You choose to adventure onward." %pC.name)
			

		def Take(self, target, objects):
			if(target in objects):
				if(objects[target].takeable):
					Say(objects[target].takeDescription)
					self.inventory[target] = objects[target]
					RemoveItem(self.location, target)
				
				else:
					Say(objects[target].takeDescription)
			
			else:
				Say("You already have the %s." %target)

		def Use(self, target, objects, objectUsed="none"):
			if(target in objects):
				if(isinstance(objects[target], Container)):
					if(objects[target].CheckIfOpened(objectUsed)):
						description, item = objects[target].DropLoot(objectUsed)
						Say(description)
						AddItem(self.location, item)
						
						if(objects[target].replaceProp != ""):
							RemoveItem(self.location, objects[target].replaceProp)
						
						AddItem(self.location, objects[target].GenerateProp())
					
					else:
						Say("You need something else here...")
				
				elif(isinstance(objects[target], TransportProp)):
					if(objects[target].CheckIfOpened(objectUsed)):
						Say(objects[target].usableItems[objectUsed])
						SetRoomAttribute(self.location, objects[target].destinationDirection, objects[target].destinationName)
						AddItem(self.location, objects[target].GenerateProp())
					
					else:
						Say("You need something else here...")
					
				else:
					Say("That isn't going to work.")
			
			else:
				Say("The use of items from the inventory is only supported in the 'do ____ WITH <item>' fashion at this point.")
			
		COMMANDS = {
		"attack": {
			"aliases": {
				"attack", 
				"kill", 
				"fight", 
				"break", 
				"smash", 
				"crush", 
				"hit", 
				"tear", 
				"rip", 
				"shred", 
				"destroy"
			},
			"function": Attack
		},
		
		"drop": {
			"aliases": {
				"drop", 
				"leave", 
				"place", 
				"abandon", 
				"throw"
			},
			"function": Drop
		},
		
		"go": {
			"aliases": {
				"go", 
				"head", 
				"travel", 
				"walk", 
				"move", 
				"run"
			},
			"function": Go
		},
		
		"help": {
			"aliases": {
				"help"
			},
			"function": Help
		},
		
		"hold": {
			"aliases": {
				"hold", 
				"pull", 
				"put", 
				"equip", 
				"deequip", 
				"remove", 
				"store"
			},
			"function": Hold
		},
		
		"inventory": {
			"aliases": {
				"inventory",
				"items"
			},
			"function": Inventory
		},
		
		"look": {
			"aliases": {
				"look", 
				"read", 
				"examine", 
				"investigate"
			},
			"function": Look
		},
		
		"quit": {
			"aliases": {
				"quit",
				"leave",
				"restart",
				"exit"
			},
			"function": Quit
		},
		
		"take": {
			"aliases": {
				"take",
				"get", 
				"pick",
				"grab"
			},
			"function": Take
		},
		
		"use": {
			"aliases": {"use"},
			"function": Use
		}
	}
		
		def UserAction(self):
			words = input("\n    >> ").lower().split(" ")
			print()
			
			foundCommmand = False
			isComplex = False
			isDirective = False
			objects = GetRoomAttribute(self.location, "objects")
			commandTargets = []
		
			for word in words:	
				if((word == "using") or (word == "with")):
					commandTargets.append("with")
					isComplex = True
				
				elif(word in CHECK_DIRECTION):
					commandTargets.append(CHECK_DIRECTION[word])
					isDirective = True
					
				elif((word == "out") and (commandWord == "take")):
					commandWord = "hold"
				
				else:
					for key in list(self.COMMANDS.keys()):
						if(word in self.COMMANDS[key]["aliases"]):
							commandWord = key
							foundCommmand = True
				
					for key, value in list(self.inventory.items()):
						if(word in value.aliases):
							commandTargets.append(key)
					
					for key, value in list(objects.items()):
						if(word in value.aliases):
							commandTargets.append(key)
			
			if(not foundCommmand):
				if(isDirective):
					commandWord = "go"
					
				elif(len(words)>1):
					commandWord = "use"
				
				else:
					commandWord = "invalid"
			
			if((len(commandTargets) == 0) and (commandWord in {"help", "inventory", "quit", "look"})):
				self.COMMANDS[commandWord]["function"](self)
			
			elif((len(commandTargets) == 1) and (commandWord in {"attack", "drop", "go", "hold", "look", "take", "use"})):
				self.COMMANDS[commandWord]["function"](self, commandTargets[0], objects)
			
			elif ((((isComplex) and (len(commandTargets) == 3)) or ((isComplex is False) and (len(commandTargets) == 2))) and (commandWord in {"attack", "use"})):
				if(isComplex):
					objectUsed = commandTargets.pop(commandTargets.index("with")+1)
					commandTargets.remove("with")
					target = commandTargets[0]
					
				else:
					objectUsed = commandTargets[0]
					target = commandTargets[1]

				self.COMMANDS[commandWord]["function"](self, target, objects, objectUsed)
			
			else:
				Say("I'm sorry, I'm afraid you can't do that. Type 'help' for a list of commands. Type 'look' to see what things you can interact with. The program will try to interpret what you say even if it doesn't exactly match a command (it will interpret 'n' or 'north' as 'go north,' for example), but it can only comprehend simple sentences. Be sure to specify the targets of your commands (i.e. 'attack the goblin' rather than 'attack it').")

	pC = Player()
	print("".join(TITLE))
		
	pC.name = input("\n  What is your name adventurer?\n\n    >> ")
	print()
	Say("It is the Third of Dragonstongue in the land of Ivalice and you are walking home from a particularly lively evening at the village tavern. The sun is setting in the distance, but the sounds of the village have not subsided just yet. Your settlement is, after all, one of the most vibrant in all the land. You take a look back towards the town-- surely another drink wouldn't hurt? Alas, you think better of it and continue to follow the winding path down to the sparkling river. You have always found this route to be the most peaceful and enjoyable way to travel these parts, much unlike the main road that connects the heart of the town to the nearby castle, Hardingham Hold. Too many foreigners on those paths, and they bring nothing but trouble. You are perfectly content to go the long way if it means avoiding all that. Unfortunately for you, a drunken and unsuspecting individual makes a perfect target for immoral vagabonds...")
	pause = input("\n    Press <ENTER> to begin your quest\n")
	Say(GetRoomAttribute(pC.location, "description_Initial"))
	UpdateDescription(pC.location)
	
	while(pC.exit is False):
		pC.UserAction()