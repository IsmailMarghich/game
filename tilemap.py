import random
import pygame
from config import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                if "\n" in line:
                    line = line[0: int(len(line) - 1)]
                    self.data.append(line)
                else:
                    self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILE_SIZE
        self.height = self.tileheight * TILE_SIZE

class RandomMapMaker:
    def __init__(self, width, height):
        self.maplevel = []
        self.width = width
        self.height = height

    def randomMapMaker(self):
        self.maplevel = []
        items = []
        for x in range(300):
            items.append(".")
        for x in range(10):
            items.append("B")
        for x in range(1):
            items.append("E")
        
        for x in range(1):
            items.append("L")

        row = ""
        map_file = open("random_map.txt", "w")

        door_x = random.randint(3, self.width-3)
        door_y = random.randint(1, self.height-3)
        for y in range(self.height):
            for x in range(self.width):
                if y == 0 or x == 0 or y == self.height-1 or x == self.width-1:
                    row += "B"
                elif x == round(self.width/2) and y == round(self.height/2) and level == 0:
                    row += "P"
                else:
                    if x == door_x and y == door_y:
                        row += "D"
                    else:
                        i = random.choice(items)                 
                        row += i
            map_file.write(row)
            map_file.write("\n")                
            self.maplevel.append(row)
            row = ""
        map_file.close()
        return self.maplevel

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(WIN_WIDTH / 2)
        y = -target.rect.y + int(WIN_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIN_WIDTH), x)
        y = max(-(self.height - WIN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
    
    def set_width_height(self, width, height):
        self.width = width
        self.height = height

m = RandomMapMaker(50, 50)
m.randomMapMaker()
tilemaps = m.maplevel
blub = Map("random_map.txt")
print(blub.data)