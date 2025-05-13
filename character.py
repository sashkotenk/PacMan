import pygame

# Базовий клас для будь-якого персонажа з рухом (відповідає принципам DRY та LSP)
class Character:
    def __init__(self, x=0, y=0, speed=2.5):
        self.position = pygame.Vector2(x, y)  # Поточна позиція персонажа
        self.speed = speed                    # Швидкість руху
        self.direction = pygame.Vector2(0, 0) # Напрям руху

    def move(self):
        # Оновлюємо позицію на основі напрямку та швидкості
        self.position += self.direction * self.speed

    def update(self):
        # Метод, який можна перевизначити — за замовчуванням просто рухає об’єкт
        self.move()

    def draw(self, screen, color=(255, 255, 0)):
        # Малюємо персонажа у вигляді круга
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), 10)
