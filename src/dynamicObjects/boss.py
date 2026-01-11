import pygame
from .dynamicObject import DynamicObject, ObjectStates
from animationsystem import AnimationController, Animation
from objectTypes import GameObjectTypes



class Boss(DynamicObject):

    images = {
        "bree" : "hi"
    }
    def __init__(self, pos, name, type, width, height, game, *groups, health = 100, cor = True):
        self.x, self.y = pos
        self.x, self.y = game.screen.virtual_width//2 + 10, game.screen.virtual_height//2
        self.name = name
        self.image = pygame.Surface((35,35))
        self.mask = pygame.mask.from_surface(self.image)
        # super().__init__(x, y, self.name, type, 35, 35, game, self.image, cor = False, *groups)
        super().__init__(self.x, self.y, name, type, width=width, height=height, game = game, image = self.image, *groups)

        self.cor = True

        # self.cor_idle_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.IDLE, type = "object"), 15, extra_anim=self.assets.load_images(self.name + "_cor", state = ObjectStates.IDLE_BLINK, type="object"), rev_loop = True)
        # self.cor_idle_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.IDLE, type = "object"), 15, rev_loop = False)
        # self.cor_run_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.RUNNING, type = "object"), 5)
        # self.cor_jump_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.JUMPING, type = "object"), 10)
        # self.cor_fall_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.FALLING, type = "object"), 10)