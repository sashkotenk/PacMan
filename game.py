import pygame
import random
from pacman import PacMan            # Клас гравця (Пакмен)
from ghost import Ghost              # Клас привидів
from menu import MainMenu            # Головне меню
from menu import SubMenu             # Підменю (наприклад, пауза)
from settings import Settings        # Клас для збереження налаштувань
from wall import Wall                # Клас для відображення стін
from coin import Coin                # Клас монет

class Game:
    def __init__(self):
        pygame.init()                                      # Ініціалізація Pygame
        pygame.display.set_caption("Pac-Man")              # Назва вікна гри
        self.clock = pygame.time.Clock()                   # Годинник для контролю FPS

        self.settings = Settings()                         # Ініціалізація налаштувань гри
        self.screen = pygame.display.set_mode(self.settings.resolution)  # Розмір вікна
        self.scale_x = self.settings.resolution[0] / 640   # Масштаб по осі X
        self.scale_y = self.settings.resolution[1] / 640   # Масштаб по осі Y

        self.menu = MainMenu(self.screen, self.settings, self.change_menu)  # Головне меню
        self.current_menu = self.menu                     # Поточне активне меню

        self.pacman = PacMan(scale_x=self.scale_x, scale_y=self.scale_y)  # Створення гравця
        self.ghosts = []                                  # Список привидів
        self.walls = []                                   # Список стін
        self.coins = []                                   # Список монет
        self.running = True                               # Чи працює гра
        self.in_menu = True                               # Чи активне меню
        self.paused = False                               # Чи гра на паузі
        self.game_over = False                            # Чи гра закінчилась
        self.score = 0                                    # Поточний рахунок

        self.pause_menu = SubMenu(                        # Меню паузи
            self.screen,
            "Game Paused",
            ["Resume", "Main Menu"],
            self.handle_pause_selection
        )



        def create_maze(self):
            self.walls.clear()
            tile_size = 20
            self.maze = [
                "############################",
                "#............##............#",
                "#.####.#####.##.#####.####.#",
                "#.####.#####.##.#####.####.#",
                "#.####.#####.##.#####.####.#",
                "#..........................#",
                "#.####.##.########.##.####.#",
                "#.####.##....##....##.####.#",
                "#......##### ## #####......#",
                "######.##### ## #####.######",
                "     #.##          ##.#     ",
                "     #.## ###  ### ##.#     ",
                "######.## #      # ##.######",
                "#     .   #      #   .     #",
                "######.## #      # ##.######",
                "     #.## ######## ##.#     ",
                "     #.##          ##.#     ",
                "######.## ######## ##.######",
                "#............##............#",
                "#.####.#####.##.#####.####.#",
                "#.####.#####.##.#####.####.#",
                "#...##................##...#",
                "###.##.##.########.##.##.###",
                "#......##....##....##......#",
                "#.##########.##.##########.#",
                "#..........................#",
                "############################"
            ]
            for y, row in enumerate(self.maze):
                for x, char in enumerate(row):
                    if char == '#':
                        wall_rect = (
                            x * tile_size * self.scale_x,
                            y * tile_size * self.scale_y,
                            tile_size * self.scale_x,
                            tile_size * self.scale_y
                        )
                        self.walls.append(Wall(wall_rect))


