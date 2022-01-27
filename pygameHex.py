import pygame
from pygame.locals import *
import os
import json
import requests

# Game Initialization
pygame.init()
# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution currently locked due to background image size
screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

# Colours for quick use
white=(255, 255, 255)
black=(0, 0, 0)
grey=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "Retro.ttf"

# Game Framerate
clock = pygame.time.Clock()
FPS=30

#List of game assets
assets = ["Title.png", "bg.jpg", "hexWhite.png", "hex.png", "levelCompleteOpt1.png", "levelCompleteOpt2.png", "controlsLeft.png", "controlsRight.png", "endScreen.png", "startHex.png"]

#Image loader
class Image(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
	#Resizing function for images to be resized so many sprites are not needed for the same different sized image
	def Resize(image_file, Scale):
		toResize = pygame.image.load(image_file)
		Resized = pygame.transform.scale(toResize, (toResize.get_width()*Scale, toResize.get_height()*Scale))
		return Resized

#A simple class for fetching the level data from a json file
class Level:
	def __init__(self, level_chosen):
		self.level_chosen = level_chosen

	def levelLoader(self, fileName):
		with open(fileName, "r") as read_file:
			levelLoad = json.load(read_file)
		return levelLoad[self.level_chosen-1]


# Game BackGround
BackGround = Image("bg.jpg", [0, 0])

# Text Renderer
def text_format(message, textFont, textSize, textColour):
	newFont=pygame.font.SysFont(textFont, textSize)
	newText=newFont.render(message, 0, textColour)
	return newText


#Main Menu
def main_menu():

	menu=True
	pygame.display.set_caption("Hexagone - Main Menu")

	while menu:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					pygame.quit()
					quit()
				elif event.key==pygame.K_RETURN:
					scene = "level_select"
					menu=False

        # Main Menu UI
		screen.fill([255, 255, 255])
		screen.blit(BackGround.image,BackGround.rect)

		# Main Menu title
		HexTitle = Image("Title.png", [150, 70])
		screen.blit(HexTitle.image,HexTitle.rect)

		#Control diagrams
		controlsLeft = Image.Resize("controlsLeft.png", 0.7)
		screen.blit(controlsLeft,[0,300])

		controlsRight = Image.Resize("controlsRight.png", 0.8)
		screen.blit(controlsRight,[screen_width-controlsRight.get_width(), 375])

		startHex = Image.Resize("startHex.png", 1)
		screen.blit(startHex,[screen_width/2-startHex.get_width()/2, 300])

		pygame.display.update()
		clock.tick(FPS)
	return(scene)

def level_select():

	select=True
	i = 0
	pygame.display.set_caption("Hexagone - Level Select")

	while select:

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
			#Event handler to allow the user to navigate level selection
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_w and i > 4:
					i -= 5
				elif event.key==pygame.K_s and i < 5:
					i += 5
				elif event.key==pygame.K_a and i != 0:
					i -= 1
				elif event.key==pygame.K_d and i != 9:
					i += 1
				elif event.key==pygame.K_RETURN:
					level_chosen = i+1
					scene = "game"
					#print(level_chosen)
					select=False
				elif event.key==pygame.K_ESCAPE:
					pygame.quit()
					quit()


		levels = ["1","2","3","4","5","6","7","8","9","10"]

		# Level Select UI
		screen.fill([255,255,255])
		screen.blit(BackGround.image,BackGround.rect)

		# Displaying hexagons and text on the screen to create a UI
		for j in range(0,5):
			levelHex = Image.Resize("hex.png", 1)
			screen.blit(levelHex,[screen_width/6 * (j+1) - (levelHex.get_width()/2) + 10, 315 - (levelHex.get_height()/2)])
			if j == i:
				level_current = text_format(levels[j], font, 55, white)
			else:
				level_current = text_format(levels[j], font, 55, black)

			screen.blit(level_current, [screen_width/6 * (j+1), 300])

		for k in range(5,10):
			levelHex = Image.Resize("hex.png", 1)
			screen.blit(levelHex,[screen_width/6 * (k-4) - (levelHex.get_width()/2) + 10, 465 - (levelHex.get_height()/2)])
			if  k == i:
				level_current = text_format(levels[k], font, 55, white)
			else:
				level_current = text_format(levels[k], font, 55, black)
			if levels[k] != "10":
				screen.blit(level_current, [screen_width/6 * (k-4), 450])
			else:
				screen.blit(level_current, [screen_width/6 * (k-4) - 10, 450])


		# Level Select title
		HexTitle = Image("Title.png", [150, 40])
		screen.blit(HexTitle.image,HexTitle.rect)

		pygame.display.update()
		clock.tick(FPS)

	return(scene, level_chosen)

def game(level_chosen):

	game = True
	#print(level_chosen)
	caption = ("Hexagone - Level " + str(level_chosen))

	#Hexagon Positions
	game_hex=Image.Resize("hex.png",0.8)
	hexX = screen_width/6
	hexY = screen_height/2
	hex_positions = [[(hexX - game_hex.get_width()/2), (hexY - game_hex.get_height()/2)],
	[hexX, (hexY - 3*game_hex.get_height()/4)],
	[hexX, (hexY - game_hex.get_height()/4)],
	[(hexX + game_hex.get_width()/2), (hexY - game_hex.get_height())],
	[(hexX + game_hex.get_width()/2), (hexY - game_hex.get_height()/2)],
	[(hexX + game_hex.get_width()/2), (hexY)],
	[(hexX + game_hex.get_width()), (hexY - 5*game_hex.get_height()/4)],
	[(hexX + game_hex.get_width()), (hexY - 3*game_hex.get_height()/4)],
	[(hexX + game_hex.get_width()), (hexY - game_hex.get_height()/4)],
	[(hexX + game_hex.get_width()), (hexY + game_hex.get_height()/4)],
	[(hexX + 3*game_hex.get_width()/2), (hexY - 3*game_hex.get_height()/2)],
	[(hexX + 3*game_hex.get_width()/2), (hexY - game_hex.get_height())],
	[(hexX + 3*game_hex.get_width()/2), (hexY - game_hex.get_height()/2)],
	[(hexX + 3*game_hex.get_width()/2), (hexY)],
	[(hexX + 3*game_hex.get_width()/2), (hexY + game_hex.get_height()/2)],
	[(hexX + 2*game_hex.get_width()), (hexY - 5*game_hex.get_height()/4)],
	[(hexX + 2*game_hex.get_width()), (hexY - 3*game_hex.get_height()/4)],
	[(hexX + 2*game_hex.get_width()), (hexY - game_hex.get_height()/4)],
	[(hexX + 2*game_hex.get_width()), (hexY + game_hex.get_height()/4)],
	[(hexX + 5*game_hex.get_width()/2), (hexY - game_hex.get_height())],
	[(hexX + 5*game_hex.get_width()/2), (hexY - game_hex.get_height()/2)],
	[(hexX + 5*game_hex.get_width()/2), (hexY)],
	[(hexX + 3*game_hex.get_width()), (hexY - 3*game_hex.get_height()/4)],
	[(hexX + 3*game_hex.get_width()), (hexY - game_hex.get_height()/4)],
	[(hexX + 7*game_hex.get_width()/2), (hexY - game_hex.get_height()/2)]]

	i=0
	opt=0

	level = Level(level_chosen)

	#Fetching the level data needed from the json file
	current_level = level.levelLoader("hexData.json")

	visited = []

	#Adding all hexagons that are not present at the start to the "visited" list, allowing for easier comparing with a completed end state
	for a in range(0,25):
		if not current_level[a]:
			visited.append(a)

	pygame.display.set_caption(caption)

	# Game Loop
	while game:

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

			#Event handler in charge of dealing with inputs during the game. Due to movement in 6 directions great specification is needed
			#An alternative to this is to hard code each hexagon using classes to know the hexagons they are connected to. Mouse controls are also an option
			if event.type==pygame.KEYDOWN and (len(visited) != 24 or i != 24):
				if event.key==pygame.K_w and i != 0 and i != 24:
					if i == 2 and current_level[1]:
						visited.append(i)
						current_level[i] = False
						i = 1
					elif i < 6 and i > 3 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1
					elif i < 10 and i > 6 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1
					elif i < 15 and i > 10 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1
					elif i < 19 and i > 15 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1
					elif i < 22 and i > 19 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1
					elif i < 24 and i > 22 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1

				elif event.key==pygame.K_s and i != 0 and i != 24:
					if i == 1 and current_level[2]:
						visited.append(i)
						current_level[i] = False
						i = 2
					elif i > 2 and i < 5 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1
					elif i > 5 and i < 9 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1
					elif i > 9 and i < 14 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1
					elif i > 14 and i < 18 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1
					elif i > 18 and i < 21 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1
					elif i > 21 and i < 23 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1

				elif event.key==pygame.K_q and i != 0:
					if i == 2 and current_level[0]:
						visited.append(i)
						current_level[i] = False
						i = 0
					elif i > 3 and i < 6 and current_level[i-3]:
						visited.append(i)
						current_level[i] = False
						i -= 3
					elif i > 6 and i < 10 and current_level[i-4]:
						visited.append(i)
						current_level[i] = False
						i -= 4
					elif i > 10 and i < 15 and current_level[i-5]:
						visited.append(i)
						current_level[i] = False
						i -= 5

					elif i > 14 and i < 19 and current_level[i-5]:
						visited.append(i)
						current_level[i] = False
						i -= 5
					elif i > 18 and i < 22 and current_level[i-4]:
						visited.append(i)
						current_level[i] = False
						i -= 4
					elif i > 21 and i < 24 and current_level[i-3]:
						visited.append(i)
						current_level[i] = False
						i -= 3
					elif i == 24 and current_level[22]:
						visited.append(i)
						current_level[i] = False
						i = 22

				elif event.key==pygame.K_e and i != 24:
					if i == 0 and current_level[1]:
						visited.append(i)
						current_level[i] = False
						i = 1
					elif i > 0 and i < 3 and current_level[i+2]:
						visited.append(i)
						current_level[i] = False
						i += 2
					elif i > 2 and i < 6 and current_level[i+3]:
						visited.append(i)
						current_level[i] = False
						i += 3
					elif i > 5 and i < 10 and current_level[i+4]:
						visited.append(i)
						current_level[i] = False
						i += 4

					elif i > 10 and i < 15 and current_level[i+4]:
						visited.append(i)
						current_level[i] = False
						i += 4
					elif i > 15 and i < 19 and current_level[i+3]:
						visited.append(i)
						current_level[i] = False
						i += 3
					elif i > 19 and i < 22 and current_level[i+2]:
						visited.append(i)
						current_level[i] = False
						i += 2
					elif i > 22 and i < 24 and current_level[i+1]:
						visited.append(i)
						current_level[i] = False
						i += 1

				elif event.key==pygame.K_a and i != 0:
					if i == 1 and current_level[0]:
						visited.append(i)
						current_level[i] = False
						i = 0
					elif i > 2 and i < 5 and current_level[i-2]:
						visited.append(i)
						current_level[i] = False
						i -= 2
					elif i > 5 and i < 9 and current_level[i-3]:
						visited.append(i)
						current_level[i] = False
						i -= 3
					elif i > 9 and i < 14 and current_level[i-4]:
						visited.append(i)
						current_level[i] = False
						i -= 4

					elif i > 14 and i < 19 and current_level[i-4]:
						visited.append(i)
						current_level[i] = False
						i -= 4
					elif i > 18 and i < 22 and current_level[i-3]:
						visited.append(i)
						current_level[i] = False
						i -= 3
					elif i > 21 and i < 24 and current_level[i-2]:
						visited.append(i)
						current_level[i] = False
						i -= 2
					elif i == 24 and current_level[i-1]:
						visited.append(i)
						current_level[i] = False
						i -= 1

				elif event.key==pygame.K_d and i != 24:
					if i == 0 and current_level[2]:
						visited.append(i)
						current_level[i] = False
						i = 2
					elif i > 0 and i < 3 and current_level[i+3]:
						visited.append(i)
						current_level[i] = False
						i += 3
					elif i > 2 and i < 6 and current_level[i+4]:
						visited.append(i)
						current_level[i] = False
						i += 4
					elif i > 5 and i < 10 and current_level[i+5]:
						visited.append(i)
						current_level[i] = False
						i += 5

					elif i > 9 and i < 14 and current_level[i+5]:
						visited.append(i)
						current_level[i] = False
						i += 5
					elif i > 14 and i < 18 and current_level[i+4]:
						visited.append(i)
						current_level[i] = False
						i += 4
					elif i > 18 and i < 21 and current_level[i+3]:
						visited.append(i)
						current_level[i] = False
						i += 3
					elif i > 21 and i < 23 and current_level[i+2]:
						visited.append(i)
						current_level[i] = False
						i += 2

				elif event.key==pygame.K_r:
					game = False
					scene = "game"

				elif event.key==pygame.K_ESCAPE:
					pygame.quit()
					quit()

			elif event.type==pygame.KEYDOWN and i == 24 and len(visited) == 24:
				if event.key==pygame.K_ESCAPE:
					pygame.quit()
					quit()

				elif level_chosen != 10:
					if event.key==pygame.K_RETURN:
						if opt == 0:
							game = False
							scene = "main_menu"
						elif opt == 1:
							game = False
							scene = "game"
							level_chosen += 1

					elif event.key==pygame.K_w or event.key==pygame.K_e or event.key==pygame.K_q or event.key==pygame.K_a or event.key==pygame.K_s or event.key==pygame.K_d:
						if opt == 0:
							opt = 1
						elif opt == 1:
							opt = 0
				else:
					if event.key==pygame.K_RETURN:
						game = False
						scene = "main_menu"








		screen.fill([255,255,255])
		screen.blit(BackGround.image,BackGround.rect)

		#Displaying remaining hexagons and currently selected one as highlighted
		for j in range(0,25):
			if j == i:
				game_hex=Image.Resize("hexWhite.png",0.8)
			else:
				game_hex=Image.Resize("hex.png",0.8)
			if current_level[j] == True:
				screen.blit(game_hex,hex_positions[j])

		#Completion Screen
		if i == 24 and len(visited) == 24 and level_chosen != 10:
			current_level[i] = False
			if opt == 0:
				levelComplete = Image.Resize("levelCompleteOpt1.png", 1)
			else:
				levelComplete = Image.Resize("levelCompleteOpt2.png", 1)
			screen.blit(levelComplete, [screen_width/2 - levelComplete.get_width()/2, screen_height/2 - levelComplete.get_height()/2])

		elif i == 24 and len(visited) == 24 and level_chosen == 10:
			current_level[i] = False
			endScreen = Image.Resize("endScreen.png", 1)
			screen.blit(endScreen, [screen_width/2 - endScreen.get_width()/2, screen_height/2 - endScreen.get_height()/2])


		pygame.display.update()
		clock.tick(FPS)

	return scene, level_chosen

#A basic scene controller deciding which screen it should be showing
def controller():
	scene = "main_menu"
	play = True
	while play:
		if scene == "main_menu":
			scene = main_menu()
		elif scene == "level_select":
			scene, level_chosen = level_select()
		elif scene == "game":
			scene, level_chosen = game(level_chosen)

#A function to ensure all assets necessary to run the game are in the folder with it.
def getAssets():
	for asset in assets:
		try:
			image = pygame.image.load(asset)
		except:
			with open(asset, "wb") as f:
				f.write(requests.get("https://github.com/Chrome599/Hexagone/raw/master/" + asset).content)
	try:
		with open("hexData.json", "r") as read_file:
			jsonCheck = json.load(read_file)
	except:
		with open("hexData.json", "wb") as f:
			f.write(requests.get("https://raw.githubusercontent.com/Chrome599/Hexagone/master/hexData.json").content)

#class Hexagon:
#	def __init__(self, active, connected):
#		self.active = active
#		self.connected = connected
#	def connection(self, direction):
#		return self.connected[direction]

#class LevelConnections:
#	def __init__(self, hexagons):
#		self.hexagons = {}
#		for hexagon, i in enumerate(hexagons):
#			self.hexagons[i] = hexagon

getAssets()
controller()
pygame.quit()
