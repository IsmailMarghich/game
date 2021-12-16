import pygame
import os

from pygame import sprite

'''
TO DO:
Make the tile selector store the 
following values in an organized way:

###
grid location of the tile
pixel location of the tile
filename of the spritesheet
grid location in the spritesheet file

'''
pygame.init()

WIN_WIDTH = 1024
WIN_HEIGHT = 768

window = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("Map Maker By MOB")

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

map_file = open("new_map.txt", "a")

running = True

mode = "file selector"

menu_box = pygame.Surface((500,600))
menu_box.fill(WHITE)
font = pygame.font.SysFont("consolas",20)
menu_text = font.render("File Selector",False,BLACK)
menu_box.blit(menu_text,(20,15))
menu_text = font.render("Press Enter To Select File",False,BLACK)
menu_box.blit(menu_text,(20,550))
file_view = pygame.Surface([600,500])

cursor_loc = [0,0]
cursor_offset = [0,0]
cursor_box = pygame.Surface([400,50])
cursor = pygame.Surface((32,32))

file_selection = 0
selected_file = ""

files = []
for x in os.listdir("img"):
    if x[-3:] == "png":
        files.append(x)

def get_sprite(file, x, y):
        sheet = pygame.image.load(f"img/{file}")
        sprite = pygame.Surface([32, 32])
        sprite.blit(sheet, (0,0), (x, y, 32, 32))
        sprite.set_colorkey(BLACK)
        return sprite

while running:
    window.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if mode == "file selector":
                if event.key == pygame.K_UP:
                    if file_selection <= 0:
                        file_selection = len(files)-1
                    else:
                        file_selection -= 1
                if event.key == pygame.K_DOWN:
                    if file_selection >= len(files)-1:
                        file_selection = 0
                    else:
                        file_selection += 1
                if event.key == pygame.K_RETURN:
                    selected_file = files[file_selection]
                    mode = "tile selector"
            
            if mode == "tile selector":
                if event.key == pygame.K_ESCAPE:
                    mode = "file selector"
                
                if event.key == pygame.K_SPACE:
                    mode = "map editor"
                    cursor.blit(get_sprite(selected_file,cursor_loc[0],cursor_loc[1]),(0,0))
                    cursor_loc = [0,0]
                
                if event.key == pygame.K_RIGHT:
                    if cursor_loc[0] >= spritesheet.get_width()-32:
                        cursor_loc[0] = spritesheet.get_width()-32
                        cursor_offset[0] = int(cursor_loc[0]/32)
                    else:
                        cursor_loc[0] += 32
                        cursor_offset[0] = int(cursor_loc[0]/32)
                if event.key == pygame.K_LEFT:
                    if cursor_loc[0] <= 0:
                        cursor_loc[0] = 0
                        cursor_offset[0] = int(cursor_loc[0]/32)
                    else:
                        cursor_loc[0] -= 32
                        cursor_offset[0] = int(cursor_loc[0]/32)
                if event.key == pygame.K_DOWN:
                    if cursor_loc[1] >= spritesheet.get_height()-32:
                        cursor_loc[1] = spritesheet.get_height()-32
                        cursor_offset[1] = int(cursor_loc[1]/32)
                    else:
                        cursor_loc[1] += 32
                        cursor_offset[1] = int(cursor_loc[1]/32)
                if event.key == pygame.K_UP:
                    if cursor_loc[1] <= 0:
                        cursor_loc[1] = 0
                        cursor_offset[1] = int(cursor_loc[1]/32)
                    else:
                        cursor_loc[1] -= 32
                        cursor_offset[1] = int(cursor_loc[1]/32)
            
            if mode == "map editor":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    if cursor_loc[0] >= WIN_WIDTH-32:
                        cursor_loc[0] = WIN_WIDTH-32
                        cursor_offset[0] = int(cursor_loc[0]/32)
                    else:
                        cursor_loc[0] += 32
                        cursor_offset[0] = int(cursor_loc[0]/32)
                if keys[pygame.K_LEFT]:
                    if cursor_loc[0] <= 0:
                        cursor_loc[0] = 0
                        cursor_offset[0] = int(cursor_loc[0]/32)
                    else:
                        cursor_loc[0] -= 32
                        cursor_offset[0] = int(cursor_loc[0]/32)
                if keys[pygame.K_DOWN]:
                    if cursor_loc[1] >= WIN_HEIGHT-32:
                        cursor_loc[1] = WIN_HEIGHT-32
                        cursor_offset[1] = int(cursor_loc[1]/32)
                    else:
                        cursor_loc[1] += 32
                        cursor_offset[1] = int(cursor_loc[1]/32)
                if keys[pygame.K_UP]:
                    if cursor_loc[1] <= 0:
                        cursor_loc[1] = 0
                        cursor_offset[1] = int(cursor_loc[1]/32)
                    else:
                        cursor_loc[1] -= 32
                        cursor_offset[1] = int(cursor_loc[1]/32)
                
                if event.key == pygame.K_ESCAPE:
                    mode = "tile selector"  

    if mode == "file selector":
        file_view.fill(WHITE)
        for index,file in enumerate(files):
            txt = font.render(file,True,BLACK)
            file_view.blit(txt,(20,40+30*index-1))
        file_view.fill(BLACK,rect=pygame.Rect(10,40+30*file_selection-1,5,20))
        menu_box.blit(file_view,(80,80))
        menu_box.blit(menu_text,(20,550))
        window.blit(menu_box,((WIN_WIDTH-500)/2,(WIN_HEIGHT-600)/2))
    
    if mode == "tile selector":
        cursor.fill((0,0,200))
        cursor.set_alpha(150)
        spritesheet = pygame.image.load("img/"+selected_file).convert()
        
        cursor_loc_txt = font.render(f"POSITION: {cursor_loc}", True, WHITE)
        cursor_offset_txt = font.render(f"OFFSET: {cursor_offset}", True, WHITE)
        cursor_box.fill(BLACK)
        cursor_box.blit(cursor_loc_txt,(0,10))
        cursor_box.blit(cursor_offset_txt,(0,30))
        window.blit(cursor_box,(WIN_WIDTH-220,20))
        window.blit(spritesheet,(0,0))
        window.blit(cursor, cursor_loc)
    
    if mode == "map editor":
        cursor_loc_txt = font.render(f"POSITION: {cursor_loc}", True, WHITE)
        cursor_offset_txt = font.render(f"OFFSET: {cursor_offset}", True, WHITE)
        cursor_box.fill(BLACK)
        cursor_box.blit(cursor_loc_txt,(0,10))
        cursor_box.blit(cursor_offset_txt,(0,30))
        window.blit(cursor_box,(WIN_WIDTH-420,20))
        window.blit(cursor, cursor_loc)
    
    pygame.display.update()
