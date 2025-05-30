import pygame
import heapq
from character import Character


class Ghost(Character):
    def __init__(self, x, y, speed=2):
        super().__init__(x, y, speed)
        self.path = []
        self.path_update_timer = 0
        self.image = pygame.image.load("assets/ghost.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def draw(self, screen, color=None):
        screen.blit(self.image, (self.position.x - 15, self.position.y - 15))

    def find_path(self, target_pos, walls, other_ghosts):
        # обчислення стартової і цільової позиції у координатах сітки
        start = (int(self.position.x) // 20, int(self.position.y) // 20)
        goal = (int(target_pos.x) // 20, int(target_pos.y) // 20)

        def neighbors(pos):
            x, y = pos
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # рух по 4х напрямках
                nx, ny = x + dx, y + dy
                blocked = any(w.rect.collidepoint(nx * 20 + 10, ny * 20 + 10) for w in walls) #перевірка чи нова позиція заблокована стіною
                # перевірка чи позиція зайнята іншим привидом
                occupied = any(
                    (int(g.position.x) // 20, int(g.position.y) // 20) == (nx, ny)
                    for g in other_ghosts if g is not self
                )
                if not blocked and not occupied:
                    yield (nx, ny)

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal: # якщо досягнута ціль — зупиняємось
                break
            for next in neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + abs(goal[0] - next[0]) + abs(goal[1] - next[1])
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        # побудова шляху від цілі до старту
        path = []
        current = goal
        while current and current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        # перетворення шляху з координат сітки в пікселі
        self.path = [pygame.Vector2(x * 20 + 10, y * 20 + 10) for x, y in path]

    def update(self, pacman, walls, other_ghosts):
        self.path_update_timer += 1
        if self.path_update_timer >= 15:
            self.find_path(pacman.position, walls, other_ghosts)
            self.path_update_timer = 0

        if self.path:
            next_cell = self.path[0]
            # продовження руху
            if self.position.distance_to(next_cell) < 5:
                self.position = next_cell
                self.path.pop(0)
            elif self.path:
                direction = (self.path[0] - self.position).normalize()
                if abs(direction.x) > abs(direction.y):
                    direction.y = 0
                else:
                    direction.x = 0
                self.position += direction * self.speed