import pygame

#клас монети
class Coin:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)  #позиція
        self.radius = 5                       #радіус кола
        self.collected = False                #чи зібрана монета

    def draw(self, screen):
        #малювання монети, якщо вона ще не зібрана
        if not self.collected:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.radius)