import pygame

class Screen:
    def __init__(self):
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Dave and the Secret Chord")
        self.SCREEN_WIDTH = infoObject.current_w
        self.SCREEN_HEIGHT = infoObject.current_h
        # self.width = self.SCREEN_WIDTH *.50
        # self.height = self.SCREEN_HEIGHT*.50
        self.width = 1440
        self.height = 768
        self.display = pygame.display.set_mode((self.width, self.height))
        # self.display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.virtual_width, self.virtual_height = 480, 256
        self.game_surface = pygame.Surface((self.virtual_width, self.virtual_height))

        self.camera = pygame.math.Vector2(0,0)


    def blit(self, surface, pos_or_rect, parallax_offset=1):
        if isinstance(pos_or_rect, pygame.Rect):
            draw_rect = pos_or_rect.copy()
            draw_rect.topleft = (round(draw_rect.x - self.camera.x * parallax_offset), round(draw_rect.y - self.camera.y))
            self.game_surface.blit(surface, draw_rect)
        else:
            draw_pos = (round(pos_or_rect[0] - self.camera.x * parallax_offset), round(pos_or_rect[1] - self.camera.y))
            self.game_surface.blit(surface, draw_pos)

    
    def set_to_screen(self):
        
        scale_x = self.width / self.virtual_width
        scale_y = self.height / self.virtual_height

        scale = min(scale_x, scale_y)

        scaled_width = int(self.virtual_width * scale)
        scaled_height = int(self.virtual_height * scale)

        offset_x = (self.width - scaled_width) // 2
        offset_y = (self.height - scaled_height) // 2

        scaled_surface = pygame.transform.scale(self.game_surface, (scaled_width, scaled_height))
        self.display.fill((0,0,0))

        self.display.blit(scaled_surface, (offset_x, offset_y))

        pygame.display.flip()
        
