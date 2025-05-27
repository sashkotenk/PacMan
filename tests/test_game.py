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
@pytest.fixture
def pacman():
    return PacMan()

@pytest.fixture
def ghost():
    return Ghost(40, 40)

@pytest.fixture
def character():
    return Character(10, 10, speed=2)

