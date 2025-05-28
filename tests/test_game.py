import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pygame
from unittest import mock
import collections

pygame.init()
pygame.display.set_mode((1, 1)) 

# Мокаємо завантаження зображень
pygame_image_load_mock = mock.Mock(return_value=pygame.Surface((1, 1)))
mock.patch('pygame.image.load', pygame_image_load_mock).start()

from character import Character
from pacman import PacMan
from ghost import Ghost
from coin import Coin
from walls import Wall


# ----------- FIXTURES --------------
# заготовки об’єктів, які використовуються в тестах
@pytest.fixture
def pacman():
    # створюємо екземпляр PacMan для кожного тесту
    return PacMan()

@pytest.fixture
def ghost():
    return Ghost(40, 40)

# створює базовий Character на позиції (10,10) з швидкістю 2
@pytest.fixture
def character():
    return Character(10, 10, speed=2)

# ----------- PARAMETRIZED TESTS --------------
# параметризовані тести перевіряють рух Character у 4 напрямках
@pytest.mark.character
@pytest.mark.parametrize("direction,expected", [
    (pygame.Vector2(1, 0), pygame.Vector2(12, 10)),
    (pygame.Vector2(0, -1), pygame.Vector2(10, 8)),
    (pygame.Vector2(-1, 0), pygame.Vector2(8, 10)),
    (pygame.Vector2(0, 1), pygame.Vector2(10, 12)),
])
def test_character_movement_param(character, direction, expected):
    # встановлюємо напрямок і викликаємо рух
    character.direction = direction
    character.move()
    assert character.position == expected

# ----------- CHARACTER --------------
@pytest.mark.character
def test_character_movement(character):
    character.direction = pygame.Vector2(1, 0)
    character.move()
    assert character.position == pygame.Vector2(12, 10)


# ----------- PACMAN -----------------
@pytest.mark.pacman
def test_pacman_initial_position(pacman):
    assert pacman.position == pygame.Vector2(320, 240)

@pytest.mark.pacman
def test_pacman_handle_event(pacman):
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    pacman.handle_event(event)
    assert pacman.direction == pygame.Vector2(-1, 0)

@pytest.mark.pacman
def test_pacman_update_keys(monkeypatch, pacman):
    # Мокаем get_pressed, чтобы вернуть "нажатую" клавишу K_RIGHT
    fake_keys = collections.defaultdict(int)
    fake_keys[pygame.K_RIGHT] = 1

    monkeypatch.setattr(pygame, "key", mock.MagicMock(get_pressed=lambda: fake_keys))
    pacman.update([])

    assert pacman.direction == pygame.Vector2(1, 0)

# ----------- GHOST ------------------
# тест базового пошуку шляху у Ghost
@pytest.mark.ghost
def test_ghost_pathfinding_basic(ghost):
    target = Character(80, 40)
    walls = []
    ghost.find_path(target.position, walls, [ghost])
    assert len(ghost.path) > 0
    assert isinstance(ghost.path[0], pygame.Vector2)


# ----------- COIN -------------------
@pytest.mark.coin
def test_coin_initial_state():
    coin = Coin(100, 100)
    assert coin.position == pygame.Vector2(100, 100)
    assert not coin.collected


# ----------- WALL -------------------
@pytest.mark.wall
def test_wall_creation():
    wall = Wall((10, 20, 30, 40))
    assert isinstance(wall.rect, pygame.Rect)
    assert wall.rect.x == 10 and wall.rect.y == 20
