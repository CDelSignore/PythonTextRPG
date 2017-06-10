from objects import *

def AddItem(location, item):
	roomManager[location]["objects"][item.name] = item

def GetRoomAttribute(location, attribute):
	return roomManager[location][attribute]	
	
def RemoveItem(location, itemName):
	del roomManager[location]["objects"][itemName]	
	
def SetRoomAttribute(location, attribute, value):
	roomManager[location][attribute] = value
	
def UpdateDescription(location):
	roomManager[location]["initial"] = False

roomManager = {
	"Forest Clearing": {
		"isRoom": True,
		"initial": True,
		"description_Initial": "You awake in a forest clearing. You are unsure how you got here, but you seem to recall something attacking the band of raiders who kidnapped you. You take a moment to regain your senses and you take a look around. The clearing is empty except for a large old tree that stands apart from the rest. The forest around the clearing is thick, but seems thinnest in the north.",
		"description_Default": "You are now back at the empty clearing where you first awoke.",
		
		"north": "Cave Entrance",
		"south": "Overgrown Forest",
		"east": "Overgrown Forest",
		"west": "Overgrown Forest",
		
		"objects": {
			"tree": tree,
			"forest": forest
		}
	},
	
	"Overgrown Forest": {
		"isRoom": False,
		"initial": True,
		"description_Initial": "The forest is overgrown with bushes and trees. You cannot make significant progress.",
		"description_Default": "The forest is too overgrown. Trekking further is a futile task.",
	},
		
	"Cave Entrance": {
		"isRoom": True,
		"initial": True,
		"description_Initial": "You hack your way through the forest to the north until you come across a large cave. You aren't sure, but there appear to be signs of a struggle at the entrance, as if someone was dragged in. At the mouth of the cave there is an ornate chest.",
		"description_Default": "The cave entrance. Something feels...off.",
		
		"north": "Cave Foyer",
		"south": "Forest Clearing",
		"east": "Overgrown Forest",
		"west": "Overgrown Forest",
		
		"objects": {
			"cave": cave,
			"chest": chest,
			"forest": forest
		}
	},
	
	"Cave Foyer": {
		"isRoom": True,
		"initial": True,
		"description_Initial": "You walk into the cave. As soon as you step foot into the cave, you feel as though you are embraced by some unseen dreadful force. Recognising your nerves, you explore the rest of the room cautiously. There is a piece of crumpled parchment laying on the floor in the center of the room that looks as though it were tossed there hastily. You also notice two moderately well-hidden doors: one to the east and one to the west.",
		"description_Default": "You are back at the opening of the cave.",
		
		"north": "Cave Wall",
		"south": "Cave Entrance",
		"east": "Storage Room",
		"west": "Crypt Entrance",
		
		"objects": {
			"cave": cave,
			"note": note
		}
	},
	
	"Cave Wall": {
		"isRoom": False,
		"initial": True,
		"description_Initial": "As you approach the cave wall you notice that it has been chiseled. This is certainly not a natural formation.",
		"description_Default": "The cave wall blocks your path.",
	},
	
	"Crypt Entrance": {
		"isRoom": True,
		"initial": True,
		"description_Initial": "The room you enter has a fowl stench to it. To the south is a door, in front of which stands a small creature (goblin). It has not taken any notice of you.",
		"description_Default": "You are back in the stinky room to the west of the mouth of the cave. In front of the southern door is a green figure. His back is turned to you and you have not alerted him.",
		
		"north": "Cave Wall",
		"south": "Door",
		"east": "Cave Foyer",
		"west": "Cave Wall",
		
		"objects": {
			"door": door,
			"goblin": goblin
		}
	},
	
	"Door": {
		"isRoom": False,
		"initial": True,
		"description_Initial": "A large oak door bars your path.",
		"description_Default": "You need to find some way through the door.",
	},
	
	"Storage Room": {
		"isRoom": True,
		"initial": True,
		"description_Initial": "You go through the door to the east. Inside you see what strikes you as an improvised storage room. Crates are stacked unorderly on all three walls. There is a shelf on the far wall, and something is sitting on top just out of reach.",
		"description_Default": "The storage room. Something sits just out of reach on a shelf on the far wall.",
		
		"north": "StoreRoom Wall",
		"south": "StoreRoom Wall",
		"east": "StoreRoom Wall",
		"west": "Cave Foyer",
		
		"objects": {
			"cave": cave,
			"crate": crate,
			"shelf": shelf,
			"mystery item": mysteryItem
		}		
	},
	
	"StoreRoom Wall": {
		"isRoom": False,
		"initial": True,
		"description_Initial": "The crates are piled high in front of the wall. You wouldn't be able to go that way anyways though.",
		"description_Default": "The storage room wall blocks your path.",
	},
	
	"Crypts": {
		"isRoom": True,
		"initial": True,
		"description_Initial": "So...this is as far as Collin got. A little underwhelming perhaps, but the goal of the portrait was coding the engine and not a game itself. It also didn't help that Collin's ACTUAL portrait broke a couple days before the deadline, leaving almost no time to complete this. Thanks for playing though! Please use the QUIT command to reset the game for someone else.",
		"description_Default": "That's all folks, please use QUIT to reset the game.",
		
		"north": "Crypt Entrance",
		"south": "Cave Wall",
		"east": "Cave Wall",
		"west": "Cave Wall",
		
		"objects": {}
	}
}