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

    def spawn_ghosts(self):
        count = 2 if self.settings.difficulty == 1 else 3
        base_speed = 1.5
        speed = base_speed if self.settings.difficulty == 1 else base_speed * 1.2
        self.ghosts.clear()

        # збираємо всі вільні клітини, де нема стіни
        valid_positions = []
        tile_size = 20
        for y, row in enumerate(self.maze):
            for x, char in enumerate(row):
                if char == '.':  # вільно
                    scaled_x = x * tile_size * self.scale_x
                    scaled_y = y * tile_size * self.scale_y
                    pos = pygame.Vector2(scaled_x + 10, scaled_y + 10)
                    if not any(w.rect.collidepoint(pos.x, pos.y) for w in self.walls):
                        valid_positions.append((scaled_x, scaled_y))

        # випадково вибираємо позиції привидів
        random.shuffle(valid_positions)
        for i in range(min(count, len(valid_positions))):
            x, y = valid_positions[i]
            self.ghosts.append(Ghost(x, y, speed))   

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

    def spawn_coins(self):
        self.coins.clear()
        tile_size = 20
        for y, row in enumerate(self.maze):
            for x, char in enumerate(row):
                if char == '.':
                    scaled_x = x * tile_size * self.scale_x + tile_size // 2 * self.scale_x
                    scaled_y = y * tile_size * self.scale_y + tile_size // 2 * self.scale_y
                    coin_rect = pygame.Rect(scaled_x - 5, scaled_y - 5, 10, 10)
                    self.coins.append(Coin(scaled_x, scaled_y))

    def run(self):
        # Головний цикл гри
        while self.running:
            if self.in_menu:
                self.handle_menu_events()
                self.current_menu.display_menu()
            elif self.game_over:
                self.handle_game_over_events()
                self.display_game_over()
            elif self.paused:
                self.handle_pause_events()
                self.pause_menu.display_menu()
            else:
                self.handle_game_events()
                self.update_game()
                self.draw_game()

            pygame.display.flip()      # Оновлення екрану
            self.clock.tick(60)        # Затримка для 60 FPS

    def handle_menu_events(self):
        # Обробка подій в меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if isinstance(self.current_menu, SubMenu):
                    if event.key == pygame.K_UP:
                        self.current_menu.navigate(-1)
                    elif event.key == pygame.K_DOWN:
                        self.current_menu.navigate(1)
                    elif event.key == pygame.K_RETURN:
                        self.current_menu.select_option()
                    elif event.key == pygame.K_ESCAPE:
                        self.current_menu.callback = None
                        self.current_menu = self.menu
                elif isinstance(self.current_menu, MainMenu):
                    if event.key == pygame.K_UP:
                        self.menu.navigate(-1)
                    elif event.key == pygame.K_DOWN:
                        self.menu.navigate(1)
                    elif event.key == pygame.K_RETURN:
                        result = self.menu.select_option()
                        if result == "start":
                            self.start_new_game()
                        elif result == "exit":
                            self.running = False

    def handle_game_events(self):
        # Обробка подій під час гри
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                else:
                    self.pacman.handle_event(event)

    def handle_pause_events(self):
        # Обробка подій у меню паузи
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pause_menu.navigate(-1)
                elif event.key == pygame.K_DOWN:
                    self.pause_menu.navigate(1)
                elif event.key == pygame.K_RETURN:
                    self.pause_menu.select_option()

    def handle_pause_selection(self, option):
        # Обробка вибору пункту в меню паузи
        if option == "Resume":
            self.paused = False
        elif option == "Main Menu":
            self.in_menu = True
            self.paused = False
            self.current_menu = self.menu

    def handle_game_over_events(self):
        # Обробка подій після завершення гри
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.in_menu = True
                    self.game_over = False
                    self.score = 0
                    self.pacman = PacMan(scale_x=self.scale_x, scale_y=self.scale_y)

    def start_new_game(self): # ініціалізація нової гри
        
        self.scale_x = self.settings.resolution[0] / 640
        self.scale_y = self.settings.resolution[1] / 480
        self.create_maze()
        self.spawn_coins()
        self.spawn_ghosts()
        self.pacman = PacMan(scale_x=self.scale_x, scale_y=self.scale_y)
        self.in_menu = False
        self.game_over = False
        self.paused = False
        self.score = 0
    

    def update_game(self): # оновлення стану гри
        
        self.pacman.update(self.walls)

        for ghost in self.ghosts:
            ghost.update(self.pacman, self.walls, self.ghosts)

        if all(coin.collected for coin in self.coins):
            self.game_over = True
            self.display_win_screen()

        for coin in self.coins:
            if not coin.collected and self.pacman.position.distance_to(coin.position) < 20:
                if self.is_coin_reachable(coin):  # перевірка доступності монети
                    coin.collected = True
                    self.score += 1

        for ghost in self.ghosts:
            if self.pacman.position.distance_to(ghost.position) < 20:
                self.game_over = True

    def draw_game(self): # вивід об'єктів гри
        self.screen.fill(self.settings.bg_color)
        for wall in self.walls:
            wall.draw(self.screen)
        for coin in self.coins:
            coin.draw(self.screen)
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen, (255, 0, 0))

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Coins: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_pause(self): # вивід тексту "пауза"
        font = pygame.font.SysFont(None, 72)
        pause_text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(pause_text, (220, 200))

    def display_game_over(self): # вивід екрану поразки
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(text, (180, 180))

        small_font = pygame.font.SysFont(None, 48)
        menu_text = small_font.render("Press ENTER to return to Menu", True, (255, 255, 255))
        self.screen.blit(menu_text, (100, 300))

    def display_win_screen(self): # вивід екрану перемоги
        self.screen.fill((0, 100, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("You Won!", True, (255, 255, 0))
        self.screen.blit(text, (200, 180))
        pygame.display.flip()
        pygame.time.delay(2000)
        self.in_menu = True
        self.game_over = False