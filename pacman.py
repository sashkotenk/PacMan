import pygame
from character import Character

class PacMan(Character):
    def __init__(self, scale_x=1, scale_y=1):
        self.scale_x = scale_x
        self.scale_y = scale_y
        start_x = 320 * scale_x
        start_y = 240 * scale_y
        super().__init__(start_x, start_y, speed=1.5)
        self.direction = pygame.Vector2(0, 0)


