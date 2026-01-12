import pygame
from objectTypes import GameObjectTypes
from animationsystem import AnimationController
from enums import ObjectStates, Instruments
from animationsystem import StateMachine


from dynamicObjects.hitbox import Hitbox

class DynamicObject(pygame.sprite.Sprite):
    G = 400

    def __init__(self, x, y, name, type, width, height, game, image, visible, *groups, health = 100, cor = False, ):
        super().__init__(*groups)

        self.image = image
        self.backup = self.image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = visible

        mask_rect = self.mask.get_bounding_rects()[0]  # relative to mask
        # distance from left edge of rect to leftmost opaque pixel
        self.mask_offset_left = mask_rect.left
        # distance from right edge of rect to rightmost opaque pixel
        self.mask_offset_right = self.rect.width - mask_rect.right
        # distance from top of rect to top opaque pixel
        self.mask_offset_top = mask_rect.top
        # distance from bottom of rect to bottom opaque pixel
        self.mask_offset_bottom = self.rect.height - mask_rect.bottom




        self.instrument_iter = iter(Instruments)
        self.current_instrument = next(self.instrument_iter)

        #body hitboxes
        self.hitbox = Hitbox(self.image, True, self.rect)
        # self.hitboxes = [
        #     [pygame.Rect(10, 5, 15, 15), True],
        #     [pygame.Rect(10, 20, 15, 15), True]
        # ]
        self.hitboxes = {
            "head" : pygame.Rect(10, 5, 14, 15),
            "body" : pygame.Rect(10, 20, 15, 10),
            "feet" : pygame.Rect(14, 30, 8, 5)
        }


        #states
        self.attacking = False
        self.dashing = False
        self.crouching = False
        self.jumping = False

        self.can_jump = True
        self.can_dash = True

        # position, physics
        self.vel = pygame.Vector2(0,0)
        self.speed = 50
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0

        #tracking things
        self.grounded_timer = .1
        self.center = pygame.math.Vector2(self.rect.center)
        self.radius = self.height//2


        # game variables
        self.name = name
        self.health = health
        self.type = type
        self.game = game
        self.assets = game.assets
        self.state = ObjectStates.IDLE
        
        if name is None:
            self.name = pygame.Surface((50,50))
            self.name.fill((255,0,0))
        else:
            self.name = name

        #animation variables
        self.draw_timer = 0
        self.backwards = False
        self.image_array = None
        self.animation_stall = 0
        self.objectState = ObjectStates.IDLE
        self.cor = cor
        self.image_index = 0

        anims_needed = [state for state in ObjectStates]
        instruments = [instrument for instrument in Instruments]

        self.animationController = AnimationController(type= "object", rev_loop = True, anims_needed=anims_needed, instruments = instruments, assets = self.game.assets, name =self.name)

        self.col = {'up': False, 'down': False, 'left': False, 'right': False}


        self.colliding_text = ''

        self.max_height = 10000000


        self.closeTiles = []

    def rects_update(self):
        self.mask_rect = self.mask.get_bounding_rects()[0]
        self.mask_rect = self.mask_rect.move(self.rect.topleft)

    def setImage(self, reset, dt):
        self.image = self.animationController.animate(dt, self.state, self.current_instrument, reset)

        if self.dx < 0:
            self.backwards = True
        elif self.dx > 0:
            self.backwards = False
        
        if self.backwards:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, game, tilemap, dt, movement=(0,0), freeze = False):

        self.closeTiles = []

        hit_rect = self.hitboxes["head"]
        head_world_rect = pygame.Rect(self.rect.x + hit_rect.x, self.rect.y + hit_rect.y, hit_rect.width, hit_rect.height)

        for tile in game.tilemap.tiles_around(head_world_rect):
            # tile.image = pygame.Surface((16,16))
            self.closeTiles.append(tile)

        self.col = {'up': False, 'down': False, 'left': False, 'right': False}

        self.colliding_text = " "

        
        self.dx = (movement[0] * self.speed + self.vel[0]) * dt
        self.rect.x += self.dx

        for collide_tile in self.closeTiles:
            tile_box = collide_tile.hitbox.tile_hitbox
            world_tile = pygame.Rect(collide_tile.rect.x + tile_box.x, collide_tile.rect.y + tile_box.y, tile_box.width, tile_box.height)

            hit_rect = self.hitboxes["body"]
            left_world_rect = pygame.Rect(self.rect.x + hit_rect.x, self.rect.y + hit_rect.y, hit_rect.width//2, hit_rect.height)
            right_world_rect = pygame.Rect(self.rect.x + hit_rect.x + hit_rect.width//2, self.rect.y + hit_rect.y, hit_rect.width//2, hit_rect.height)
            
            if self.dx < 0 and left_world_rect.colliderect(world_tile):
                offset = left_world_rect.left - self.rect.left
                self.rect.left = world_tile.right - offset
                self.dx = 0
                self.vel[0] = 0
                break
            elif self.dx > 0 and right_world_rect.colliderect(world_tile):
                offset = self.rect.right - right_world_rect.right
                self.rect.right = world_tile.left + offset
                self.dx = 0
                self.vel[0] = 0
                break
        
    
        self.vel[1] = min(self.vel[1] + DynamicObject.G * dt, 200)
        self.dy = (self.vel[1] + movement[1] * self.speed) * dt

        self.rect.y += self.dy

        for collide_tile in self.closeTiles:            
            tile_box = collide_tile.hitbox.tile_hitbox
            world_tile = pygame.Rect(collide_tile.rect.x + tile_box.x, collide_tile.rect.y + tile_box.y, tile_box.width, tile_box.height)

            hit_rect = self.hitboxes["head"]
            head_world_rect = pygame.Rect(self.rect.x + hit_rect.x, self.rect.y + hit_rect.y, hit_rect.width, hit_rect.height)

            hit_rect = self.hitboxes["feet"]
            feet_world_rect = pygame.Rect(self.rect.x + hit_rect.x, self.rect.y + hit_rect.y, hit_rect.width, hit_rect.height)

            if self.dy < 0 and head_world_rect.colliderect(world_tile):
                self.rect.top = world_tile.bottom
                self.vel[1] = 0
                self.dy = 0
                break
            elif self.dy > 0 and feet_world_rect.colliderect(world_tile):
                self.col["down"] = True
                self.rect.bottom = world_tile.top
                self.vel[1] = 0
                self.dy = 0
                break
        
        # if self.max_height > self.rect.y:
        #     self.max_height = self.rect.y
        #     print(self.rect.y)
        
    def post_update(self, dt):
        
        if self.col['down']:
            self.grounded_timer = .1
        else:
            self.grounded_timer = max(0, self.grounded_timer - dt)

        self.draw_timer += 1

        self.state = StateMachine.stateChange(self, self.state, (self.dx, self.dy), self.freezing)

        prev_state = self.state
        
        
        reset = prev_state is not self.state
        # if reset:
        #     print(self.state)

        self.setImage(reset, dt)


        mask_rect = self.mask.get_bounding_rects()[0]  # relative to mask
        # distance from left edge of rect to leftmost opaque pixel
        self.mask_offset_left = mask_rect.left
        # distance from right edge of rect to rightmost opaque pixel
        self.mask_offset_right = self.rect.width - mask_rect.right
        # distance from top of rect to top opaque pixel
        self.mask_offset_top = mask_rect.top
        # distance from bottom of rect to bottom opaque pixel
        self.mask_offset_bottom = self.rect.height - mask_rect.bottom


        
        


        self.jumping = False


        
        


            
