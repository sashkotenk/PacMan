import pygame

class MainMenu:
    def __init__(self, screen, settings, change_menu_callback):
        self.options = ["Start Game", "Background Color", "Difficulty", "Resolution", "Exit"]
        self.selected_index = 0
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.SysFont(None, 40)
        self.bg_colors = [(0, 0, 0), (50, 50, 100), (20, 60, 20), (120, 0, 120)]
        self.difficulties = ["Easy", "Hard"]
        self.resolutions = [(640, 480), (800, 600), (1024, 768), (1280, 720)]
        self.change_menu_callback = change_menu_callback  

    def display_menu(self):
        self.screen.fill(self.settings.bg_color)
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (100, 100 + i * 50))
        pygame.display.flip()

    def navigate(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def select_option(self):
        selected = self.options[self.selected_index]
        if selected == "Start Game":
            return "start"
        elif selected == "Exit":
            return "exit"
        elif selected == "Background Color":
            self.change_menu_callback(SubMenu(
                self.screen,
                "Choose Background Color",
                [f"Color {i + 1}" for i in range(len(self.bg_colors))],
                lambda choice: self.set_bg_color(choice)
            ))
        elif selected == "Difficulty":
            self.change_menu_callback(SubMenu(
                self.screen,
                "Choose Difficulty",
                self.difficulties,
                lambda choice: self.set_difficulty(choice)
            ))
        elif selected == "Resolution":
            self.change_menu_callback(SubMenu(
                self.screen,
                "Choose Resolution",
                [f"{w}x{h}" for w, h in self.resolutions],
                lambda choice: self.set_resolution(choice)
            ))
        return None

    def set_bg_color(self, label):
        index = int(label.split()[-1]) - 1
        self.settings.change_bg_color(self.bg_colors[index])
        self.change_menu_callback(self)

    def set_difficulty(self, label):
        diff = 1 if label == "Easy" else 2
        self.settings.adjust_difficulty(diff)
        self.change_menu_callback(self)

    def set_resolution(self, label):
        width, height = map(int, label.lower().split('x'))
        resolution = self.settings.set_resolution((width, height))
        self.screen = pygame.display.set_mode(resolution)
        self.change_menu_callback(self)



class SubMenu:
    def __init__(self, screen, title, options, callback):
        self.screen = screen
        self.title = title
        self.options = options
        self.selected = 0
        self.callback = callback
        self.font = pygame.font.SysFont(None, 40)

    def display_menu(self):
        self.screen.fill((0, 0, 0))
        title_text = self.font.render(self.title, True, (255, 255, 255))
        self.screen.blit(title_text, (100, 50))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (100, 100 + i * 50))

        pygame.display.flip()

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def select_option(self):
        self.callback(self.options[self.selected])
