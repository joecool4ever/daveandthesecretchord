import pygame
from dynamicObjects import *
from item import Item
from enums import Instruments
from spriteGroups import *
from objectTypes import GameObjectTypes

class EntityManager():

    def __init__(self, game):
        self.game = game

        #spriteGroups
        self.all_sprites = SpriteGroup()
        self.tiles = SpriteGroup()
        self.visible_tiles = SpriteGroup()
        self.actors = SpriteGroup()
        self.activeActors = SpriteGroup()
        self.visible_sprites = VisibleSprites()
        self.items = SpriteGroup()


    def update(self, camera):

        #Item Collisions
        hits = pygame.sprite.spritecollide(self.game.dave, self.items, dokill=True, collided = pygame.sprite.collide_mask)

        for hit in hits:
            self.game.dave.collect_item(hit.name)

        #visibleSprites
        self.visible_sprites.empty()

        camera_rect = pygame.Rect(camera.x, camera.y, 480, 256)

        for sprite in self.all_sprites.sprites():
            if sprite.rect.colliderect(camera_rect):

                if sprite not in self.tiles:
                    self.visible_sprites.add(sprite)
                else:
                    self.visible_tiles.add(sprite)


    #spawn Entities
    def spawnEntity(self, type, pos, subtype = None):

        entity = None

        match type:
            case GameObjectTypes.DAVE:
                entity = Dave(self.game, pos, current_instrument=Instruments.MIC)
            
            case GameObjectTypes.ITEMS:
                if subtype == "coin":
                    entity = Item(27, 27, "coin", self.game.assets, pos)
                    
                elif "note" in subtype:
                    entity = Item(27, 27, subtype, self.game.assets, pos)

                self.items.add(entity)

        
        self.all_sprites.add(entity)
        self.actors.add(entity)
        self.activeActors.add(entity)
        if entity.visible:
            self.visible_sprites.add(entity)
        return entity



    #remove Dave

    #respawn Dave

    #remove Enemies from existence
    