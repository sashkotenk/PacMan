import pygame
from character import Character

class PacMan(Character):
    def __init__(self, scale_x=1, scale_y=1):
        self.scale_x = scale_x
        self.scale_y = scale_y
        start_x = 320 * scale_x
        start_y = 240 * scale_y
        super().__init__(start_x, start_y, speed=1.5)
        self.lives = 3
        self.direction = pygame.Vector2(0, 0)
        self.image = pygame.image.load("assets/pacman.png").convert_alpha()  # PNG з прозорістю
        self.image = pygame.transform.scale(self.image, (30, 30))  # Масштабування
    def draw(self, screen):
        screen.blit(self.image, (self.position.x - 15, self.position.y - 15))  # Центрування

