class Settings:
    def __init__(self):
        # Встановлення початкової роздільної здатності (ширина, висота)
        self.resolution = (640, 480)
        # Встановлення початкового кольору фону (чорний: RGB (0, 0, 0))
        self.bg_color = (0, 0, 0)
        # Встановлення початкового рівня складності (1 - легкий)
        self.difficulty = 1

    def set_resolution(self, resolution):
        # Зміна роздільної здатності на вказане значення
        self.resolution = resolution
        return resolution  

    def adjust_difficulty(self, level):
        # Зміна рівня складності на вказаний рівень
        self.difficulty = level

    def change_bg_color(self, color):
        # Зміна кольору фону на вказаний колір (у форматі RGB)
        self.bg_color = color