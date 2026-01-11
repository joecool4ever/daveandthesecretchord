import pygame
import os
from .tile import Tile
import random

PHYSIC_TYPES = {'grass', 'stone'}



class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.grid_width = 30
        self.grid_height = 16


        for i in range(self.grid_height):
            tile = Tile(self.game, "left_top_corner", 0, (10, i), self.game.all_sprites, self.game.tiles)
            self.tilemap["10;" + str(i)] = tile

        # for i in range(self.grid_height):
        #     tile = Tile(self.game, "right_top_corner", 0, (25, i), self.game.all_sprites, self.game.tiles)
        #     self.tilemap["25;" + str(i)] = tile
        
        for i in range(self.grid_width):
            tile = Tile(self.game, "right_top_corner", 0, (i, 5), self.game.all_sprites, self.game.tiles)
            self.tilemap[str(i) + ";5"] = tile

        

        for i in range(self.grid_width * 2):
            height = self.grid_height
            if i == 0:
                tile = Tile(self.game, "left_top_corner", 0, (0, height), self.game.all_sprites, self.game.tiles)
                self.tilemap["0;" + str(height)] = tile

                tile = Tile(self.game, "left_middle", 0, (0, height + 1), self.game.all_sprites, self.game.tiles)
                self.tilemap["0;"+ str(height + 1)] = tile

                tile = Tile(self.game, "bottom_left", 0, (0, height + 2), self.game.all_sprites, self.game.tiles)
                self.tilemap["0;"+ str(height + 2)] = tile
            elif i == self.grid_width * 2 - 1:
                tile = Tile(self.game, "right_top_corner", 0, (i, height), self.game.all_sprites, self.game.tiles)
                self.tilemap[str(i) + ";"+ str(height)] = tile

                tile = Tile(self.game, "right_middle", 0, (i, height + 1), self.game.all_sprites, self.game.tiles)
                self.tilemap[str(i) + ";"+ str(height + 1)] = tile

                tile = Tile(self.game, "bottom_right", 0, (i, height + 2), self.game.all_sprites, self.game.tiles)
                self.tilemap[str(i) + ";"+ str(height + 2)] = tile
            else:
                variant = random.randint(0,1)

                tile = Tile(self.game, "middle_top", variant, (i, height), self.game.all_sprites, self.game.tiles)
                self.tilemap[str(i) + ";" + str(height)] = tile

                tile = Tile(self.game, "true_middle", variant, (i, height + 1), self.game.all_sprites, self.game.tiles)
                self.tilemap[str(i) + ";" + str(height + 1)] = tile

                tile = Tile(self.game, "bottom_middle", variant, (i, height + 2), self.game.all_sprites, self.game.tiles)
                self.tilemap[str(i) + ";" + str(height + 2)] = tile

        self.playercoord = []
        self.tilepos = []

        # tile = Tile(self.game, "right", 0, (self.grid_width*2, self.grid_height), self.game.all_sprites, self.game.tiles)
        # self.game.all_sprites.add(tile)
        # self.game.tiles.add(tile)
        # self.tilemap[str(self.grid_width) + ";" + str(self.grid_height)] = tile

    def tiles_around(self, rect):
        tiles = []

        left_tile = rect.left // self.tile_size
        right_tile = (rect.right - 1) // self.tile_size
        top_tile = rect.top // self.tile_size
        bottom_tile = (rect.bottom - 1) // self.tile_size

        for x in range(left_tile, right_tile + 1):
            for y in range(top_tile, bottom_tile + 1):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        key = str(x + j) + ";" + str(y + i)
                        if key in self.tilemap:
                            if self.tilemap[key] not in tiles:
                                tiles.append(self.tilemap[key])
        self.tilepos = []
        for tile in tiles:
            self.tilepos.append([tile.grid_x, tile.grid_y])

        return tiles
        
    def physics_tiles(self, rect):
        tiles = []
        for tile in self.tiles_around(rect):
            if tile.type in PHYSIC_TYPES:
                tiles.append(tile)
        return tiles
