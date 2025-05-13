import pygame

class Wall:
    def __init__(self, rect):
        # Ініціалізуємо стіну як прямокутник Pygame з переданими координатами і розмірами
        self.rect = pygame.Rect(rect)

    def draw(self, screen):
        # Малюємо стіну синього кольору (RGB: 0, 0, 255) на переданому екрані
        pygame.draw.rect(screen, (0, 0, 255), self.rect)