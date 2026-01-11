import pygame

class Hitbox:

    def __init__(self, image, active, rect):
        self.image = image
        self.active = active

        self.hitboxes = {}

        self.body_mask = pygame.mask.from_surface(self.image)


        self.head_hitbox = pygame.Rect(10, 5, 15, 15)
        self.body_hitbox = pygame.Rect(10, 20, 15, 15)

        self.tile_hitbox = pygame.Rect(0, 3, rect.width, rect.height - 3)

        self.hitbox_surf = pygame.Surface((self.tile_hitbox.width, self.tile_hitbox.height), pygame.SRCALPHA)
        self.hitbox_surf.fill((0, 50, 155, 120))
        