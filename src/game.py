import os, warnings

# Hide pygame startup messages
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["PYGAME_SDL_NO_LOGGING"] = "1"

# Ignore Python warnings from certain modules
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=UserWarning)

import pygame

from utils import lerp
from enums import Instruments
from dynamicObjects import Boss, Dave
from objectTypes import GameObjectTypes
from screen import Screen
from assetload import AssetLoad
from tilesystem import Tilemap
from spriteGroup import SpriteGroup
from animationsystem import AnimationController
from background import Background
from item import Item
from hud import Hud
from utils import note_colors

assets = None

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()


        self.font = pygame.font.SysFont('Arial', 30)
        
        self.screen = Screen()

        self.assets = AssetLoad()
        self.background = Background(self.assets)

        #spriteGroups
        self.all_sprites = SpriteGroup()
        self.camera_group = SpriteGroup()
        self.tiles = SpriteGroup()
        self.character_sprites = SpriteGroup()
        self.items = SpriteGroup()

        #sprites
        self.dave = Dave(self, self.all_sprites, self.character_sprites, current_instrument=Instruments.MIC)
        self.health = Item(50, 60, "health", self.assets, (self.screen.virtual_width//2 + 100, self.screen.virtual_height//2), self.all_sprites, self.items)

        for x in range(20):
            Item(27, 27, "coin", self.assets, ((self.screen.virtual_width//2 + 120) + x * 10, self.screen.virtual_height//2 + 100), self.all_sprites, self.items)

        #hud
        self.hud = Hud(self.dave, self.screen, self.assets, self.font)


        notes_width = self.screen.virtual_width//2 + 150
        notes_height = self.screen.virtual_height//2

        for color in note_colors[:-1]:
            note = Item(27, 27, color + "note", self.assets, (notes_width, notes_height), self.items, self.all_sprites)
            notes_width += 50
        
        #focus on Dave
        self.screen.camera.x = self.dave.rect.centerx - self.screen.virtual_width // 2
        self.screen.camera.y = self.dave.rect.centery - self.screen.virtual_height // 2
        
        # self.bree = Boss((100, 20), "bree", GameObjectTypes.ENEMY, 35, 35, self)
        self.movement = [False, False]
        self.crouch_pressed = False

        self.clock = pygame.time.Clock()

        self.running = True

        self.tilemap = Tilemap(self)

        self.frames = 0





        self.freezing = False

    def run(self):
        while self.running:
            # dt = self.clock.tick(1)
            dt = self.clock.tick(60) / 1000
            if dt > 0.5:
                dt = 0
    
            self.handle_input(dt)
            self.applyPhysics(dt)
            self.handle_item_collisions(self.dave, self.items)
            self.renderScene(dt)
            
            pygame.display.flip()

            
    def handle_input(self,dt):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.attack_button_pressed = True
                    self.dave.attack(self.attack_button_pressed, dt)
                    # if self.dave.current_instrument == Instruments.TRUMPET:
                    #     self.trumpet.unpause()
                if event.button == 3:
                    try:
                        self.dave.current_instrument = next(self.dave.instrument_iter)
                    except(StopIteration):
                        self.dave.instrument_iter = iter(Instruments)
                        self.dave.current_instrument = next(self.dave.instrument_iter)
                    # if not self.dave.current_instrument == Instruments.TRUMPET:
                    #     self.trumpet.pause()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.attack_button_pressed = False
                    self.dave.attack(self.attack_button_pressed, dt)
                    # if self.dave.current_instrument == Instruments.TRUMPET:
                    #     self.trumpet.pause()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_s:
                    self.crouch_pressed = True
                    self.dave.crouch(self.crouch_pressed)
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_SPACE:
                    self.dave.jump() 
                if event.key == pygame.K_LSHIFT:
                    self.dave.dash()
                if event.key == pygame.K_p:
                    self.freezing = not self.freezing
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_s:
                    self.crouch_pressed = False
                    self.dave.crouch(self.crouch_pressed)
                    
    def applyPhysics(self,dt):
        self.items.update(dt)
        self.character_sprites.update(self,self.tilemap, dt, (self.movement[1] - self.movement[0], self.crouch_pressed), freeze = self.freezing)
        self.character_sprites.post_update(dt)
        

        # Moving the camera to player
        alpha = 1 - pow(0.9, dt * 60) 
        target = pygame.math.Vector2((self.dave.rect.x,self.dave.rect.y)) - pygame.math.Vector2(self.screen.virtual_width // 2, self.screen.virtual_height // 2)

        self.screen.camera.x = lerp(self.screen.camera.x, target.x, alpha)
        self.screen.camera.y = lerp(self.screen.camera.y, target.y, alpha)
        # self.screen.camera += (target - self.screen.camera) * alpha
        self.screen.camera.x = max(self.screen.camera.x, 0)

        self.background.updateBackgrounds()

    def handle_item_collisions(self, player, items):
        hits = pygame.sprite.spritecollide(player, items, dokill=True, collided=pygame.sprite.collide_mask)

        for hit in hits:
            self.dave.collect_item(hit.name)



    
    def renderScene(self, dt):
        self.screen.game_surface.fill((226, 255, 252)) 
        self.background.backRender(self.screen)
        for sprite in self.items.sprites():
            self.screen.blit(sprite.image, sprite.rect.topleft)
        for sprite in self.tiles.sprites():
            self.screen.blit(sprite.image, sprite.rect.topleft)
            self.screen.blit(sprite.hitbox.hitbox_surf, (sprite.rect.x, sprite.rect.y + 5))

        # create a transparent surface the size of the hitbox 
        hitbox_surf = pygame.Surface((self.dave.hitboxes["head"].width, self.dave.hitboxes["head"].height), pygame.SRCALPHA)
        b_hitbox_surf = pygame.Surface((self.dave.hitboxes["body"].width, self.dave.hitboxes["body"].height), pygame.SRCALPHA)
        f_hitbox_surf = pygame.Surface((self.dave.hitboxes["feet"].width, self.dave.hitboxes["feet"].height), pygame.SRCALPHA)



        # fill it with semi-transparent color
        hitbox_surf.fill((255, 0, 0, 120))
        b_hitbox_surf.fill((0, 0, 255, 120))
        f_hitbox_surf.fill((255, 140, 0, 120))

        self.screen.blit(self.dave.image, self.dave.rect)
        self.screen.blit(hitbox_surf, (self.dave.rect.x + self.dave.hitboxes["head"].x, self.dave.rect.y + self.dave.hitboxes["head"].y))
        self.screen.blit(b_hitbox_surf, (self.dave.rect.x + self.dave.hitboxes["body"].x, self.dave.rect.y + self.dave.hitboxes["body"].y))
        self.screen.blit(f_hitbox_surf, (self.dave.rect.x + self.dave.hitboxes["feet"].x, self.dave.rect.y + self.dave.hitboxes["feet"].y))
        
        # debug text
        dave_pos_text = self.font.render(f'{self.dave.rect.x}, {self.dave.rect.y}', True, (0,0,0))
        dave_vel_text = self.font.render(f'{self.dave.vel[0]}, {self.dave.vel[1]}', True, (0,0,0))
        dave_grounded_text = self.font.render(f'{self.dave.grounded_timer}', True, (0,0,0))
        dave_grounded_bool_text = self.font.render(f'{self.dave.col['down']}', True, (0,0,0))
        dave_crouching_text = self.font.render(f'{self.dave.crouching}', True, (0,0,0))


        # col_flag_rect = self.dave.rect.copy()
        

        self.hud.display()
        self.screen.set_to_screen()


        # self.screen.display.blit(dave_pos_text, (100,100))
        # self.screen.display.blit(dave_vel_text, (100,50))
        # self.screen.display.blit(dave_grounded_text, (100,150))
        # self.screen.display.blit(dave_grounded_bool_text, (100,200))
        # self.screen.display.blit(dave_crouching_text, (100,250))

        


        

        

Game().run()
pygame.quit()