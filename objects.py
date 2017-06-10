class Item(object): #keys/weps/etc.
	takeable = True
	
	def __init__(self, name, aliases, info_look, info_setting, breakStrength, breakDescription, takeDescription):
		self.name = name
		self.aliases = aliases
		self.info_look = info_look
		self.info_setting = info_setting
		self.breakStrength = breakStrength 
		self.breakDescription = breakDescription
		self.takeDescription = takeDescription

class Prop(object):
	takeable = False
	breakStrength = 5

	def __init__(self, name, aliases, info_look, breakDescription, takeDescription):
		self.name = name
		self.aliases = aliases
		self.info_look = info_look
		self.breakDescription = breakDescription
		self.takeDescription = takeDescription
	
class Container(Prop):
	def __init__(self, name, aliases, info_look, breakDescription, takeDescription, containsObject, usableItems, replaceProp): #usable items must be dict {ITEMNAME: OPENDESCRIPTION}
		Prop.__init__(self, name, aliases, info_look, breakDescription, takeDescription)
		self.containsObject = containsObject
		self.usableItems = usableItems
		self.replaceProp = replaceProp
	
	def CheckIfOpened(self, itemUsed):
		if(itemUsed in self.usableItems.keys()):
			return True
			
		else:
			return False
	
	def DropLoot(self, itemUsed):
		description = self.usableItems[itemUsed]
		return (description, self.containsObject)
	
	def GenerateProp(self):
		propVersion = Prop(self.name, self.aliases, self.info_look, self.breakDescription, self.takeDescription)
		return propVersion

class Enemy(Container):
	def __init__(self, name, aliases, info_look, breakDescription, takeDescription, containsObject, usableItems, replaceProp):
		Container.__init__(self, name, aliases, info_look, breakDescription, takeDescription, containsObject, usableItems, replaceProp)

class TransportProp(Prop):
	def __init__(self, name, aliases, info_look, breakDescription, takeDescription, usableItems, destinationDirection, destinationName):
		Prop.__init__(self, name, aliases, info_look, breakDescription, takeDescription)
		self.usableItems = usableItems
		self.destinationDirection = destinationDirection
		self.destinationName = destinationName

	def CheckIfOpened(self, itemUsed):
		if(itemUsed in self.usableItems.keys()):
			return True
			
		else:
			return False
			
	def GenerateProp(self):
		propVersion = Prop(self.name, self.aliases, self.info_look, self.breakDescription, self.takeDescription)
		return propVersion
			
stick = Item(
	"stick",
	{"stick", "branch", "club", "twig"},
	"A long and heavy stick. Not an ideal weapon, but could probably be used as a makeshift club.",
	" The stick remains.",
	2,
	"Small cracks appear in the wood and quickly splinter up the length of the stick. The stick is no longer usable.",
	"You pick up the stick, surprised at its modest weight. You secure it to a loop in your belt."
)

dagger = Item(
	"dagger",
	{"dagger", "knife", "shiv", "shank", "blade"},
	"An ornate dagger with a worn blade. You get the feeling that this must have been some sort of ritual dagger judging by the strange etchings on the handle. You examine the blade closely but cannot discern any meaning from the markings.",
	" The dagger still sits where you left it.",
	3,
	"The dagger's blade snaps off. The weapon is no longer effective.",
	"You take the dagger, toss it into the air for dramatic effect, and put it in your waistband."
)

key = Item(
	"key",
	{"key"},
	"A seemingly hand-forged silver key. Wrapping around the shaft of the key is a serpant, shaped in astonishing detail. If it were not for the glittering quality of the metal, you might have mistaken it for a real snake.",
	" The key glimers on the ground where you left it.",
	3,
	"The teeth snap off of the key. Not only is the asthetic ruined, but the key is also not particularly useful anymore.",
	"You take the key and drop it into your pocket for safekeeping. It'd be a shame to leave such a thing at a place such as this."
)

note = Item(
	"note",
	{"note", "paper", "parchment"},
	"You have to move your eyes quite close to the paper before you can make out the faint letters. The letter reads: 'If you are reading this, there is not much time. Please save me from the Guild-- there's money in it for you if I get out alive. I don't want them to have a single coin! Just make sure to be weary of... [The note ends here with a long trailing scribble]",
	" The tattered parchment sits delicately on the floor.",
	0,
	"The note turns to dust.",
	"As you begin to pick up the paper, you notice that it is very close to disintegrating. You proceed with extra caution and manage to roll it into a fairly sturdy form suitable for travel. You place it in your bag to keep it safe."
)

forest = Prop(
	"forest",
	{"forest", "woods", "trees"},
	"You don't know how you could've gotten here through the dense forest. As you stare off into the distance, you get the feeling you are being watched.",
	"The tree is old and strong, and you cannot do any significant damage.",
	"You cannot manage to break anything useful off the tree to take."
)

cave = Prop(
	"cave",
	{"cave", "wall", "cavern"},
	"This cave gives you the chills. Something about it just doesn't sit well with you.",
	"Unsurprisingly, the stone wall does not break.",
	"The wall is solid. There is nothing you can take from it."
)

shelf = Prop(
	"shelf",
	{"shelf", "ledge"},
	"The shelf is just out of reach. If only you had some way to get up there.",
	"The shelf is affixed securely to the wall. You cannot knock it down.",
	"The shelf is attatched to the wall, and you cannot remvoe it."
)

mysteryItem = Prop(
	"mystery item",
	{"object", "item"},
	"Whatever it is, the item sits just out of reach on the shelf.",
	"You cannot reach it.",
	"You cannot reach it."
)

tree = Container(
	"tree",
	{"tree", "trunk", "treetrunk"},
	"There is an old tree that looks like it might fall over if you hit it.",
	"The tree doesn't budge.",
	"There's no way you're grabbing a giant tree like that, even if it's old and dying.",
	stick,
	{"unarmedAttack": "You try to knock over the tree. It is surprisingly stable, but a moderately-sized branch falls in front of you."},
	""
)
		
chest = Container(
	"chest",
	{"chest", "trunk", "box", "container"},
	"The chest is old and worn, but looks as though it hasn't been opened in a while. There is a brass setting that resembles a keyhole.",
	"Despite its age, the chest is quite resilient. It does not break.",
	"The chest is far too heavy to take with you.",
	dagger,
	{"key": "You insert the key into the brass setting. Nothing happens for a moment and then the chest violently swings open, revealing an ornate dagger."},
	""
)

crate = Container(
	"crate",
	{"crate", "crates", "box", "boxes", "container", "containers", "barrel", "barrels"},
	"Crates are haphazardly arranged in the room. It appears as though someone has looted this area.",
	"One of the crates explodes into shards of splintering wood. There is nothing inside.",
	"These crates are heavy and there isn't any reason to try to carry them with you.",
	key,
	{"none": "You push some of the crates over to the shelf and climb up. You can now see that the item was a key."},
	"mystery item"
)

door = TransportProp(
	"door",
	{"door"},
	"An old oak door with silver and brass detailing. Judging by it's weathered condition, you suspect it has been there for several decades. There is a decorative keyhole above which the word 'serpēns' is stylistically carved.",
	"You attempt to knock the door off it's hinges. The door may be worn, but there is a reason it has not yet been replaced. It doesn't budge.",
	"Really? I admire your enthusiasm but you cannot take EVERYTHING with you ;)",
	{"key": "As you lift the serpantine key up to the keyhole, it flies from your hand into the lock of it's own accord. There is a clicking sound yet nothing happens. Several seconds later the key is ejected from the door and lands in your pocket. The door slowly opens."},
	"south",
	"Crypts"
)

#PLACEHOLDER
goblin = Item(
	"goblin",
	{"goblin, creature, enemy, monster, ogre, orc, guy"},
	"",
	"",
	0,
	"",
	""
)