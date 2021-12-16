import pygame
from pygame.display import update
from sprites import *
from teachers import *
from config import *
from tilemap import *
from os import path
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("pixel_font.ttf", 32)
        self.running = True
        
        self.character_spritesheet = Spritesheet("img/characterr.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.ground_spritesheet = Spritesheet("img/ground_spritesheet.png")
        self.door_spritesheet = Spritesheet("img/door_spritesheet.png")
        self.enemy_spritesheet = Spritesheet("img/enemy.png")
        self.attack_spritesheet = Spritesheet("img/attack.png")
        self.shuriken_spritesheet = Spritesheet("img/shuriken.png")
        self.intro_background = pygame.image.load("img/caland2.png").convert()

        self.enemies_left = 0

        self.load_data()
        
    def createTilemap(self, map):
        for i, row in enumerate(map):
            for j, column in enumerate(row):
                Ground(self, j, i, 1, 2)
                if column == "-":
                    Ground(self, j, i, 1, 0)
                if column == "B":
                    Block(self, j, i, 960, 544)
                if column == "E":
                    Enemy(self, j, i)                  
                    self.enemies_left += 1
                if column == "D":
                    Door(self, j, i)                 
                if column == "P":
                    Ground(self, j, i, 5, 1)
                    self.player = Player(self, j, i)
                if column == "H":
                    Human(self, j, i, create_human_spritesheet("img/hamersveld.png"), "Hello Player, Welcome to my new game called, CalandRPG")
                if column == "L":
                    Human(self, j, i, create_human_spritesheet("img/luken.png"), "Quest: kill all aliens", quest = True)
                    
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, "map.txt"))
    
    def new(self):
        #when the game starts
        self.playing = True
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.humans = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()

        self.camera = Camera(self.map.width, self.map.height)
           
        self.createTilemap(self.map.data)


    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if not self.player.freezed:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if self.player.facing == "up":
                            Interaction(self, self.player.rect.x, self.player.rect.y - TILE_SIZE)
                        if self.player.facing == "down":
                            Interaction(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                        if self.player.facing == "left":
                            Interaction(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                        if self.player.facing == "right":
                            Interaction(self, self.player.rect.x + TILE_SIZE, self.player.rect.y)

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.player.projectile_counter <= 10:
                        if self.player.facing == "up":
                            Shuriken(self, self.player.rect.x + 10, self.player.rect.y - TILE_SIZE/2)
                        if self.player.facing == "down":
                            Shuriken(self, self.player.rect.x + 10, self.player.rect.y + TILE_SIZE)
                        if self.player.facing == "left":
                            Shuriken(self, self.player.rect.x - TILE_SIZE/2, self.player.rect.y + 10)
                        if self.player.facing == "right":
                            Shuriken(self, self.player.rect.x + TILE_SIZE, self.player.rect.y + 10, )


    def update(self):
        #game loop updates
        self.all_sprites.update()
        self.camera.update(self.player)
    
    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.clock.tick(FPS)
        pygame.display.update()
        
    def main(self):
        #gameloop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def game_over(self):
        pass
    
    def intro_screen(self):
        intro = True
        
        title = self.font.render("CalandRPG", False, BLACK)
        title_rect = title.get_rect(x = int(WIN_WIDTH / 2 - title.get_width() / 2), y = 20)

        play_button = Button(int(WIN_WIDTH / 2 - 50), 100, 100, 50, WHITE, BLACK, "PLAY", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)

            pygame.display.update()



g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit
sys.exit()