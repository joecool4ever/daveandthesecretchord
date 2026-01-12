import pygame

class SpriteGroup(pygame.sprite.Group):

    def post_update(self, *args, **kwargs):
        for sprite in self.sprites():
            if hasattr(sprite, "post_update"):
                sprite.post_update(*args,**kwargs)