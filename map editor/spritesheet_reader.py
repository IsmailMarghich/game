from typing import overload
import pygame
from pygame import *
from pygame.constants import *
import os
 
pygame.init()
 
#Game Globals
running = True
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
TILESIZE = 32
 
#Window Init
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Spritesheet Reader")
font = pygame.font.SysFont("consolas",20)
mode = "menu"
menu_selection = 0
selected_file = ""
#Sprites / Rects
box = pygame.Surface([32,32])
box.fill(GREEN)
box.set_alpha(180)
 
overlay = pygame.Surface([800,600])
overlay.fill(BLACK)
overlay.set_alpha(210)
txt = font.render("Open File",True,WHITE)
overlay.blit(txt,(20,20))
txt = font.render("Mouseroot Tile Viewer",True,WHITE)
overlay.blit(txt,(500,20))
txt = font.render("Enter to Select File",True,WHITE)
overlay.blit(txt,(510,550))
files = []
file_view = pygame.Surface([600,500])
 
_x = 150
 
 
spritesheet = pygame.image.load("img/terrain.png").convert()
spritesheet.set_colorkey(BLACK)
cursor_pos = [0,0]
cursor_offset = [0,0]
 
display_window = pygame.Surface([300,75])
 
while running:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
 
            if mode == "menu":
                if event.key == pygame.K_RETURN:
                    selected_file = files[menu_selection]
                    spritesheet = pygame.image.load(f"img/{selected_file}").convert()
                    mode = "view"
 
                if event.key == pygame.K_UP:
                    if menu_selection == 0:
                        menu_selection = len(files)-1
                    else:
                        menu_selection -= 1
                if event.key == pygame.K_DOWN:
                    if menu_selection == len(files)-1:
                        menu_selection = 0
                    else:
                        menu_selection += 1
 
            if mode == "view":
                #Move Cursor
                #Up
                if event.key == pygame.K_UP:
                    if cursor_pos[1] == 0:
                        pass
                    else:
                        cursor_pos[1] -= TILESIZE
                        cursor_offset[1] -=1
                #Down
                if event.key == pygame.K_DOWN:
                    cursor_pos[1] += TILESIZE
                    cursor_offset[1] += 1
 
                #Left
                if event.key == pygame.K_LEFT:
                    if cursor_offset[0] == 0:
                        cursor_pos[0] = (TILESIZE * TILESIZE-TILESIZE)
                        cursor_pos[1] -= TILESIZE
                        cursor_offset[0] = TILESIZE
                    else:
                        cursor_pos[0] -= TILESIZE
                        cursor_offset[0] -= 1
 
                #Right
                if event.key == pygame.K_RIGHT:
                    if cursor_offset[0] == 32:
                        cursor_pos[0] = 0
                        cursor_pos[1] += TILESIZE
                        cursor_offset[0] = 0
                        #cursor_offset[1] += 1
                    else:
                        cursor_pos[0] += TILESIZE
                        cursor_offset[0] += 1
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"
 
    if mode == "view":  
        #Update
        cursor_pos_text = font.render(f"Cursor: {cursor_pos[0]},{cursor_pos[1]} ({TILESIZE} Offset)",True,WHITE)
        cursor_pos_offset = font.render(f"Offset: {cursor_offset[0]},{cursor_offset[1]}",True,WHITE)
        #Draw
        window.fill(WHITE)
        window.blit(spritesheet,(0,0))
 
        window.blit(box,cursor_pos)
        display_window.fill(BLACK)
        display_window.set_alpha(200)
        display_window.blit(cursor_pos_text,(5,5))
        display_window.blit(cursor_pos_offset,(5,25))
        window.blit(display_window,(50,50))
    if mode == "menu":
        file_view.fill(WHITE)
        files = os.listdir("img")
        for index,file in enumerate(files):
            txt = font.render(file,True,BLACK)
            file_view.blit(txt,(20,20+30*index-1))
        file_view.fill(BLACK,rect=pygame.Rect(10,20+30*menu_selection-1,5,20))
        overlay.blit(file_view,(_x,40))
        window.blit(overlay,(0,0))
    pygame.display.update()
 
pygame.quit()