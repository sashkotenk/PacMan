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
        self.image = pygame.image.load("assets/pacman.png").convert_alpha()  # PNG з прозорістю
        self.image = pygame.transform.scale(self.image, (30, 30))  # Масштабування
    def draw(self, screen):
        screen.blit(self.image, (self.position.x - 15, self.position.y - 15))  # Центрування

    def update(self, walls):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        if keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.direction.y = 1

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()


        self.position.x += self.direction.x * self.speed
        if any(wall.rect.collidepoint(self.position) for wall in walls):
            self.position.x -= self.direction.x * self.speed


        self.position.y += self.direction.y * self.speed
        if any(wall.rect.collidepoint(self.position) for wall in walls):
            self.position.y -= self.direction.y * self.speed

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = pygame.Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.direction = pygame.Vector2(1, 0)
            elif event.key == pygame.K_UP:
                self.direction = pygame.Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                self.direction = pygame.Vector2(0, 1)

