import pygame
from animationsystem import AnimationController

class Item(pygame.sprite.Sprite):
    def __init__(self, width, height, name, assets, pos, *groups):
        super().__init__(*groups)

        self.width = width
        self.height = height
        self.name = name

        self.x, self.y = pos
        self.type = "item"
        self.visible = True

        self.animationController = AnimationController(self.type, name = self.name, assets = assets)

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, game, tilemap, dt, movement=(0,0), freeze = False):
        self.image = self.animationController.animate(dt, state = self.name)
        self.mask = pygame.mask.from_surface(self.image)

