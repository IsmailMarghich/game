import pygame
from config import *
from tilemap import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.x_change = 0
        self.y_change = 0
        self.last_x_shifting = 0
        self.last_y_shifting = 0


        self.dash_cooldown = 0
        self.sprint_cooldown = 0
        self.sprinting_time = 0
        self.projectile_counter = 0
        self.freezed = False
        
        self.facing = "down"
        self.animation_loop = 1
        self.animation_speed = 0.1
        
        self.image = self.game.character_spritesheet.get_sprite(4, 1, self.width, self.height)
             
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(37, 1, 23, 31),
                                self.game.character_spritesheet.get_sprite(5, 2, 23, 30),
                                self.game.character_spritesheet.get_sprite(69, 2, 23, 30)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(37, 97, 23, 31),
                              self.game.character_spritesheet.get_sprite(5, 98, 24, 30),
                              self.game.character_spritesheet.get_sprite(68, 98, 24, 30)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(37, 33, 23, 31),
                                self.game.character_spritesheet.get_sprite(5, 34, 24, 30),
                                self.game.character_spritesheet.get_sprite(68, 34, 24, 30)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(37, 65, 23, 31),
                                self.game.character_spritesheet.get_sprite(5, 66, 24, 30),
                                self.game.character_spritesheet.get_sprite(68, 66, 24, 30)]
    
    def update(self):
        if not self.freezed:
            self.movement()
            self.animate()
            
            #move the Player object 
            self.rect.x += self.x_change
            self.collision_blocks("x")
        
            self.rect.y += self.y_change
            self.collision_blocks("y")

            self.dash_cooldown += 0.05
            
            self.last_x_shifting = self.x_change
            self.last_y_shifting = self.y_change
            self.x_change = 0
            self.y_change = 0
    
    def movement(self):
        running = False
        #create a list with all pressed buttons
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"

        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"

        if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"

        if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"

        if self.keys[pygame.K_LSHIFT] and self.sprinting_time < 10 and (self.x_change != 0 or self.y_change != 0):
            self.x_change *= 2
            self.y_change *= 2
            self.sprinting_time += 0.05
            running = True
            self.animation_speed = 0.2
        elif self.sprinting_time >= 10:
            if self.sprint_cooldown > 10:
                self.sprint_cooldown = 0
                self.sprinting_time = 0
        if not running: 
            self.sprint_cooldown += 0.05
            self.animation_speed = 0.1

        if self.keys[pygame.K_x]:
            if self.dash_cooldown >= 4 and (self.x_change != 0 or self.y_change != 0):
                if self.x_change != 0 and not running:
                    self.x_change *= 50
                elif self.x_change != 0:
                    self.x_change *= 25
                if self.y_change != 0 and not running:
                    self.y_change *= 50
                elif self.y_change != 0:
                    self.y_change *= 25
                self.dash_cooldown = 0        
        
    def collision_blocks(self, direction):
        if direction == "x":
            #Check for collision between player and blocks
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            
            #Check for collision between player and enemy
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            #Check for collision between player and blocks
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
            
            #Check for collision between player and enemy
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
        
    def animate(self):        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1
    def delete(self):
        self.kill()

class Human(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image_list, text, quest=False):
        self.game = game
        self._layer = HUMAN_LAYER
        self.groups = self.game.all_sprites, self.game.humans
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1
        
        self.image_list = image_list
        self.image = self.image_list["down"][0]
        self.text = text
        self.quest = quest
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()

    def animate(self):        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.image_list["down"][0]
            else:
                self.image = self.image_list["down"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.image_list["up"][0]
            else:
                self.image = self.image_list["up"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.image_list["right"][0]
            else:
                self.image = self.image_list["right"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.image_list["left"][0]
            else:
                self.image = self.image_list["left"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = HUMAN_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right", "up", "down"])
        self.animation_loop = 1
        self.movement_loop_x = 0
        self.movement_loop_y = 0
        self.max_travel = random.randint(10, 30)

        self.freezed = False

        self.text = "123456789012345678901234567890123456789012345678901234567890123456789012345678901"

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        if not self.freezed:
            self.movement()
            self.animate()

            self.rect.x += self.x_change 
            self.collision_blocks("x")

            self.rect.y += self.y_change
            self.collision_blocks("y")

            self.x_change = 0
            self.y_change = 0
    
    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop_x -= 1
            if self.movement_loop_x <= -self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])

        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop_x += 1
            if self.movement_loop_x >= self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])

        if self.facing == "down":
            self.y_change += ENEMY_SPEED
            self.movement_loop_y += 1
            if self.movement_loop_y >= self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])

        if self.facing == "up":
            self.y_change -= ENEMY_SPEED
            self.movement_loop_y -= 1
            if self.movement_loop_y <= -self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])
    
    def collision_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sx, sy):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(sx, sy, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sx, sy):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.image = self.game.ground_spritesheet.get_sprite(sx * 32, sy * 32, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.door_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.animations = [self.game.door_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.door_spritesheet.get_sprite(64, 0, self.width, self.height)]
        self.animation_loop = 0
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def door_open(self):
        if self.game.enemies_left <= 0:
            self.image = self.animations[math.floor(self.animation_loop)]
            if self.animation_loop < 1.9:
                self.animation_loop += 0.2

            interaction = pygame.sprite.spritecollide(self, self.game.players, False)
            if interaction:
                for b in self.game.all_sprites:
                    if b != self:
                        b.kill()
                
                self.game.createTilemap(m.randomMapMaker())
                self.kill()
    
    def update(self):
        self.door_open()

class Interaction(pygame.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.humans, False)
        if hits:
            if len(hits[0].text) > 0 and hits[0].quest:
                print(hits[0].text)
                Textbox(self.game, self.game.player.rect.x - 150, self.game.player.rect.y - 200, width = 300, height= 100, txt=hits[0].text, follow=hits[0].quest)
            elif len(hits[0].text) > 0:
                print(hits[0].text)
                Textbox(self.game, self.game.player.rect.x - 350, self.game.player.rect.y + 200, txt=hits[0].text)
    def animate(self):
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

class Shuriken(pygame.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILE_SIZE/2
        self.height = TILE_SIZE/2

        self.direction = self.game.player.facing
        self.velocity()        

        self.animation_loop = 0
        self.life_countdown = 0
        self.game.player.projectile_counter += 0

        self.image = self.game.shuriken_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animations = [self.game.shuriken_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.shuriken_spritesheet.get_sprite(17, 0, self.width, self.height),
                           self.game.shuriken_spritesheet.get_sprite(34, 0, self.width, self.height),
                           self.game.shuriken_spritesheet.get_sprite(51, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()
        self.movement()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.game.enemies_left -= 1
            self.game.player.projectile_counter -= 1
            self.kill()
        if self.life_countdown >= 20:
            self.game.player.projectile_counter -= 1
            self.kill()
        self.life_countdown += 0.1
    
    def movement(self):
        self.pos+=self.vel   #s+=u+1/2a
        self.rect.x, self.rect.y = self.pos
    
    def velocity(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        x = WIN_WIDTH/2
        y = WIN_HEIGHT/2

        self.dx = int(mouse_x - x) / 50
        self.dy = int(mouse_y - y) / 50

        vec = pygame.math.Vector2
        self.pos=vec(self.game.player.rect.center[0], self.game.player.rect.center[1])
        self.vel=vec(self.dx, self.dy) 
        
        print("Mouse pos:", mouse_x, ",", mouse_y)
        print("Player pos:", self.pos)

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.5
        if self.animation_loop >= 4:
            self.animation_loop = 0

class Textbox(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width=500, height=200, text_color=(0,0,0), txt="", txt_size=20, follow=False):
        self.game = game
        self._layer = TOP_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.follow = follow #This attritbute is to check if the textbox has to follow the player
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        if not follow:
            #Make all moving sprites stand still
            self.game.player.freezed = True
            for e in self.game.enemies:
                e.freezed = True
        
        self.txt_size = txt_size
        self.font = pygame.font.Font("pixel_font.ttf", self.txt_size)
        self.text_color = text_color
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, False, self.text_color)
        self.txt_rect = self.txt_surf.get_rect(topleft=(round(55*(self.width/500)), round(45*(self.height/200))))

        self.image = pygame.image.load("img/dialogue_box_basic.png").convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=[x,y])

        self.image.blit(self.txt_surf, self.txt_rect)

    def update(self):
        self.skip()
        if self.follow:
            self.follow_player()

    def follow_player(self):
        self.rect.x += self.game.player.last_x_shifting
        self.rect.y += self.game.player.last_y_shifting

    def skip(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #Make all moving sprites move
            self.game.player.freezed = False
            for e in self.game.enemies:
                e.freezed = False
            self.kill()

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("pixel_font.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False   