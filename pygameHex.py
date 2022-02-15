import pygame
from pygame.locals import *
import os
import json
import requests

# Game Initialization
pygame.init()
# Center the Game Application
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Game Resolution currently locked due to background image size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours for quick use
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)


# Game Fonts
font = "Retro.ttf"

# Game Framerate
clock = pygame.time.Clock()
FPS = 30

# List of game assets
assets = [
    "Title.png",
    "bg.jpg",
    "hexWhite.png",
    "hex.png",
    "levelCompleteOpt1.png",
    "levelCompleteOpt2.png",
    "controlsLeft.png",
    "controlsRight.png",
    "endScreen.png",
    "startHex.png",
    "padlock.png",
]

# A function to ensure all assets necessary to run the game are in the folder with it by downloading them off github.
def getAssets():
    for asset in assets:
        try:
            image = pygame.image.load("assets\\" + asset)
        except:
            with open((os.getcwd() + "\\assets\\" + asset), "wb") as f:
                f.write(
                    requests.get(
                        "https://raw.githubusercontent.com/Chrome599/Hexagone/master/assets/"
                        + asset
                    ).content
                )
    try:
        with open("hexData.json", "r") as read_file:
            jsonCheck = json.load(read_file)
    except:
        with open((os.getcwd() + "\\assets\\hexData.json"), "wb") as f:
            f.write(
                requests.get(
                    "https://raw.githubusercontent.com/Chrome599/Hexagone/master/assets/hexData.json"
                ).content
            )


getAssets()

# A dict containing indexs for specific hexagons, and the hexagon indexs connected to these in specific directions
connections = {
    0: {"E": 1, "D": 2},
    1: {"E": 3, "A": 0, "S": 2, "D": 4},
    2: {"Q": 0, "W": 1, "E": 4, "D": 5},
    3: {"E": 6, "A": 1, "S": 4, "D": 7},
    4: {"Q": 1, "W": 3, "E": 7, "A": 2, "S": 5, "D": 8},
    5: {"Q": 2, "W": 4, "E": 8, "D": 9},
    6: {"E": 10, "A": 3, "S": 7, "D": 11},
    7: {"Q": 3, "W": 6, "E": 11, "A": 4, "S": 8, "D": 12},
    8: {"Q": 4, "W": 7, "E": 12, "A": 5, "S": 9, "D": 13},
    9: {"Q": 5, "W": 8, "E": 13, "D": 14},
    10: {"A": 6, "S": 11, "D": 15},
    11: {"Q": 6, "W": 10, "E": 15, "A": 7, "S": 12, "D": 16},
    12: {"Q": 7, "W": 11, "E": 16, "A": 8, "S": 13, "D": 17},
    13: {"Q": 8, "W": 12, "E": 17, "A": 9, "S": 14, "D": 18},
    14: {"Q": 9, "W": 13, "E": 18},
    15: {"Q": 10, "A": 11, "S": 16, "D": 19},
    16: {"Q": 11, "W": 15, "E": 19, "A": 12, "S": 17, "D": 20},
    17: {"Q": 12, "W": 16, "E": 20, "A": 13, "S": 18, "D": 21},
    18: {"Q": 13, "W": 17, "E": 21, "A": 14},
    19: {"Q": 15, "A": 16, "S": 20, "D": 22},
    20: {"Q": 16, "W": 19, "E": 22, "A": 17, "S": 21, "D": 23},
    21: {"Q": 17, "W": 20, "E": 23, "A": 18},
    22: {"Q": 19, "A": 20, "S": 23, "D": 24},
    23: {"Q": 20, "W": 22, "E": 24, "A": 21},
    24: {"Q": 22, "A": 23},
}


# Image loader
class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    # Resizing function for images to be resized so many sprites are not needed for the same different sized image
    def Resize(image_file, Scale):
        toResize = pygame.image.load(image_file)
        Resized = pygame.transform.scale(
            toResize, (toResize.get_width() * Scale, toResize.get_height() * Scale)
        )
        return Resized


# A simple class for fetching the level data from a json file
class Level:
    def __init__(self, level_chosen):
        self.level_chosen = level_chosen

    def levelLoader(self, previous_index):
        with open(file_name, "r") as read_file:
            levelLoad = json.load(read_file)
        return levelLoad[self.level_chosen - 1]


class Hexagon:
    def __init__(self, active):
        self.active = active

    def make_inactive(self):
        self.active = False

    def make_active(self):
        self.active = True


class LevelConnections:
    def __init__(self, hexagons, visited, starting_index=0):
        self.hexagons = hexagons
        self.visited = visited
        self.index = starting_index

    def possible_move(self, direction, undoButton):
        try:
            if self.hexagons[connections[self.index][direction]].active:
                next_index = connections[self.index][direction]
                self.hexagons[self.index].make_inactive()
                undoButton.newMove(self.index)
                self.index = next_index
                self.visited += 1
                if self.visited == 24 and self.index == 24:
                    self.hexagons[self.index].make_inactive()
        except:
            pass
        return self.index

    def is_active(self, index):
        return self.hexagons[index].active

    def number_visited(self):
        return self.visited

    def undo_move(self, previous_index):
        self.visited -= 1
        self.index = previous_index
        return self.hexagons[previous_index].make_active()


class PlayerData:
    def __init__(self):
        try:
            with open("playerData.json", "r") as read_file:
                self.unlocks = json.load(read_file)
        except:
            default = [i == 0 for i in range(10)]
            with open("playerData.json", "w") as outfile:
                json.dump(default, outfile)
            self.unlocks = default

    def getUnlocked(self, index):
        return self.unlocks[index]

    def dataUpdater(self, index):
        self.unlocks[index] = True

    def externalUpdater(self):
        os.remove("playerData.json")
        with open("playerData.json", "w") as outfile:
            json.dump(self.unlocks, outfile)


# A stack class to implement an undo button feature
class UndoStack:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.previousMoves = []

    # A function for adding the index of the last visited hexagon to the list of previous moves
    def newMove(self, new):
        if len(self.previousMoves) <= self.maxsize:
            self.previousMoves.append(new)

    # A function for popping the top item in the stack, before performing the undo function and returning the popped value
    def undo(self, connectionsStart):
        previous_index = self.previousMoves.pop()
        connectionsStart.undo_move(previous_index)
        return previous_index

    # Checks if the stack is empty or not
    def empty(self):
        if len(self.previousMoves) == 0:
            return True
        else:
            return False


# Hexagon Positions for game

game_hex = Image.Resize("assets\\hex.png", 0.8)
hexX = screen_width / 6
hexY = screen_height / 2
hex_positions = [
    [(hexX - game_hex.get_width() / 2), (hexY - game_hex.get_height() / 2)],
    [hexX, (hexY - 3 * game_hex.get_height() / 4)],
    [hexX, (hexY - game_hex.get_height() / 4)],
    [(hexX + game_hex.get_width() / 2), (hexY - game_hex.get_height())],
    [(hexX + game_hex.get_width() / 2), (hexY - game_hex.get_height() / 2)],
    [(hexX + game_hex.get_width() / 2), (hexY)],
    [(hexX + game_hex.get_width()), (hexY - 5 * game_hex.get_height() / 4)],
    [(hexX + game_hex.get_width()), (hexY - 3 * game_hex.get_height() / 4)],
    [(hexX + game_hex.get_width()), (hexY - game_hex.get_height() / 4)],
    [(hexX + game_hex.get_width()), (hexY + game_hex.get_height() / 4)],
    [(hexX + 3 * game_hex.get_width() / 2), (hexY - 3 * game_hex.get_height() / 2)],
    [(hexX + 3 * game_hex.get_width() / 2), (hexY - game_hex.get_height())],
    [(hexX + 3 * game_hex.get_width() / 2), (hexY - game_hex.get_height() / 2)],
    [(hexX + 3 * game_hex.get_width() / 2), (hexY)],
    [(hexX + 3 * game_hex.get_width() / 2), (hexY + game_hex.get_height() / 2)],
    [(hexX + 2 * game_hex.get_width()), (hexY - 5 * game_hex.get_height() / 4)],
    [(hexX + 2 * game_hex.get_width()), (hexY - 3 * game_hex.get_height() / 4)],
    [(hexX + 2 * game_hex.get_width()), (hexY - game_hex.get_height() / 4)],
    [(hexX + 2 * game_hex.get_width()), (hexY + game_hex.get_height() / 4)],
    [(hexX + 5 * game_hex.get_width() / 2), (hexY - game_hex.get_height())],
    [(hexX + 5 * game_hex.get_width() / 2), (hexY - game_hex.get_height() / 2)],
    [(hexX + 5 * game_hex.get_width() / 2), (hexY)],
    [(hexX + 3 * game_hex.get_width()), (hexY - 3 * game_hex.get_height() / 4)],
    [(hexX + 3 * game_hex.get_width()), (hexY - game_hex.get_height() / 4)],
    [(hexX + 7 * game_hex.get_width() / 2), (hexY - game_hex.get_height() / 2)],
]


# Game BackGround
BackGround = Image("assets\\bg.jpg", [0, 0])

# Text Renderer
def text_format(message, textFont, textSize, textColour):
    newFont = pygame.font.SysFont(textFont, textSize)
    newText = newFont.render(message, 0, textColour)
    return newText


unlocked = PlayerData()

# Main Menu
def main_menu():

    menu = True
    pygame.display.set_caption("Hexagone - Main Menu")

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                unlocked.externalUpdater()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unlocked.externalUpdater()
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_RETURN:
                    scene = "level_select"
                    menu = False

                    # Main Menu UI
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        # Main Menu title
        HexTitle = Image("assets\\Title.png", [150, 70])
        screen.blit(HexTitle.image, HexTitle.rect)

        # Control diagrams
        controlsLeft = Image.Resize("assets\\controlsLeft.png", 0.7)
        screen.blit(controlsLeft, [40, 300])

        controlsRight = Image.Resize("assets\\controlsRight.png", 0.8)
        screen.blit(controlsRight, [screen_width - controlsRight.get_width() + 20, 320])

        startHex = Image.Resize("assets\\startHex.png", 1)
        screen.blit(startHex, [screen_width / 2 - startHex.get_width() / 2, 300])

        pygame.display.update()
        clock.tick(FPS)
    return scene


def level_select():

    select = True
    i = 0
    pygame.display.set_caption("Hexagone - Level Select")

    while select:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                unlocked.externalUpdater()
                pygame.quit()
                quit()
            # Event handler to allow the user to navigate level selection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and i > 4:
                    if unlocked.getUnlocked(i - 5):
                        i -= 5
                elif event.key == pygame.K_s and i < 5:
                    if unlocked.getUnlocked(i + 5):
                        i += 5
                elif event.key == pygame.K_a and i != 0:
                    if unlocked.getUnlocked(i - 1):
                        i -= 1
                elif event.key == pygame.K_d and i != 9:
                    if unlocked.getUnlocked(i + 1):
                        i += 1
                elif event.key == pygame.K_RETURN:
                    level_chosen = i + 1
                    scene = "game"
                    # print(level_chosen)
                    select = False
                elif event.key == pygame.K_ESCAPE:
                    unlocked.externalUpdater()
                    pygame.quit()
                    quit()

        levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        # Level Select UI
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        # Displaying hexagons and text on the screen to create a UI
        for j in range(0, 5):
            levelHex = Image.Resize("assets\\hex.png", 1)
            screen.blit(
                levelHex,
                [
                    screen_width / 6 * (j + 1) - (levelHex.get_width() / 2) + 10,
                    315 - (levelHex.get_height() / 2),
                ],
            )
            if j == i:
                level_current = text_format(levels[j], font, 55, white)
            else:
                level_current = text_format(levels[j], font, 55, black)
            if unlocked.getUnlocked(j):
                screen.blit(level_current, [screen_width / 6 * (j + 1), 300])
            else:
                padlock = Image.Resize("assets\\padlock.png", 0.5)
                screen.blit(padlock, [screen_width / 6 * (j + 1), 300])

        for k in range(5, 10):
            levelHex = Image.Resize("assets\\hex.png", 1)
            screen.blit(
                levelHex,
                [
                    screen_width / 6 * (k - 4) - (levelHex.get_width() / 2) + 10,
                    465 - (levelHex.get_height() / 2),
                ],
            )
            if k == i:
                level_current = text_format(levels[k], font, 55, white)
            else:
                level_current = text_format(levels[k], font, 55, black)
            if levels[k] != "10" and unlocked.getUnlocked(k):
                screen.blit(level_current, [screen_width / 6 * (k - 4), 450])
            elif unlocked.getUnlocked(k):
                screen.blit(level_current, [screen_width / 6 * (k - 4) - 10, 450])
            else:
                padlock = Image.Resize("assets\\padlock.png", 0.5)
                screen.blit(padlock, [screen_width / 6 * (k - 4), 450])

        # Level Select title
        HexTitle = Image("assets\\Title.png", [150, 40])
        screen.blit(HexTitle.image, HexTitle.rect)

        pygame.display.update()
        clock.tick(FPS)

    return (scene, level_chosen)


def game(level_chosen):

    game = True
    # print(level_chosen)
    caption = "Hexagone - Level " + str(level_chosen)

    i = 0
    opt = 0

    level = Level(level_chosen)

    # Fetching the level data needed from the json file
    current_level = level.levelLoader("assets\\hexData.json")

    visited_start = 0

    # Adding all hexagons that are not present at the start to the "visited" list, allowing for easier comparing with a completed end state
    for a in range(0, 25):
        if not current_level[a]:
            visited_start += 1

    hexagons = []

    for hexagon in range(0, 25):
        hexagons.append(Hexagon(current_level[hexagon]))

    connectionsStart = LevelConnections(hexagons, visited_start)

    undoButton = UndoStack(24)

    pygame.display.set_caption(caption)

    # Game Loop
    while game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                unlocked.externalUpdater()
                pygame.quit()
                quit()

            # Event handler in charge of dealing with inputs during the game. Due to movement in 6 directions great specification is needed
            # An alternative to this is to hard code each hexagon using classes to know the hexagons they are connected to. Mouse controls are also an option
            if event.type == pygame.KEYDOWN and (
                connectionsStart.number_visited() != 24 or i != 24
            ):
                if event.key == pygame.K_w and i != 0 and i != 24:
                    i = connectionsStart.possible_move("W", undoButton)

                elif event.key == pygame.K_q and i != 0:
                    i = connectionsStart.possible_move("Q", undoButton)

                elif event.key == pygame.K_e and i != 24:
                    i = connectionsStart.possible_move("E", undoButton)

                elif event.key == pygame.K_a and i != 0:
                    i = connectionsStart.possible_move("A", undoButton)

                elif event.key == pygame.K_d and i != 24:
                    i = connectionsStart.possible_move("D", undoButton)

                elif event.key == pygame.K_s and i != 0 and i != 24:
                    i = connectionsStart.possible_move("S", undoButton)

                elif event.key == pygame.K_r:
                    game = False
                    scene = "game"

                elif event.key == pygame.K_ESCAPE:
                    unlocked.externalUpdater()
                    pygame.quit()
                    quit()

                elif event.key == pygame.K_b:
                    game = False
                    scene = "level_select"

                elif event.key == pygame.K_LEFT:
                    if not undoButton.empty():
                        i = undoButton.undo(connectionsStart)

            elif (
                event.type == pygame.KEYDOWN
                and i == 24
                and connectionsStart.number_visited() == 24
            ):
                if event.key == pygame.K_ESCAPE:
                    unlocked.externalUpdater()
                    pygame.quit()
                    quit()

                elif level_chosen != 10:
                    if event.key == pygame.K_RETURN:
                        if opt == 0:
                            game = False
                            scene = "main_menu"
                        elif opt == 1:
                            game = False
                            scene = "game"
                            level_chosen += 1

                    elif (
                        event.key == pygame.K_w
                        or event.key == pygame.K_e
                        or event.key == pygame.K_q
                        or event.key == pygame.K_a
                        or event.key == pygame.K_s
                        or event.key == pygame.K_d
                    ):
                        if opt == 0:
                            opt = 1
                        elif opt == 1:
                            opt = 0
                else:
                    if event.key == pygame.K_RETURN:
                        game = False
                        scene = "main_menu"

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        # Displaying remaining hexagons and currently selected one as highlighted
        for j in range(0, 25):
            if j == i:
                game_hex = Image.Resize("assets\\hexWhite.png", 0.8)
            else:
                game_hex = Image.Resize("assets\\hex.png", 0.8)
            if connectionsStart.is_active(j):
                screen.blit(game_hex, hex_positions[j])

        # Completion Screen
        if i == 24 and connectionsStart.number_visited() == 24 and level_chosen != 10:
            unlocked.dataUpdater(level_chosen)
            if opt == 0:
                levelComplete = Image.Resize("assets\\levelCompleteOpt1.png", 1)
            else:
                levelComplete = Image.Resize("assets\\levelCompleteOpt2.png", 1)
            screen.blit(
                levelComplete,
                [
                    screen_width / 2 - levelComplete.get_width() / 2,
                    screen_height / 2 - levelComplete.get_height() / 2,
                ],
            )

        elif i == 24 and connectionsStart.number_visited() == 24 and level_chosen == 10:
            endScreen = Image.Resize("assets\\endScreen.png", 1)
            screen.blit(
                endScreen,
                [
                    screen_width / 2 - endScreen.get_width() / 2,
                    screen_height / 2 - endScreen.get_height() / 2,
                ],
            )

        pygame.display.update()
        clock.tick(FPS)

    return scene, level_chosen


# A basic scene controller deciding which screen it should be showing
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


controller()
pygame.quit()
