import pygame
import heapq
from character import Character


class Ghost(Character):
    def __init__(self, x, y, speed=2):
        super().__init__(x, y, speed)
        self.path = []
        self.path_update_timer = 0
        self.image = pygame.image.load("assets/ghost.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def draw(self, screen, color=None):
        screen.blit(self.image, (self.position.x - 15, self.position.y - 15))