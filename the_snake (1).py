
import random

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализация игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод отрисовки."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, snake_positions=None):
        """Инициализация яблока."""
        super().__init__((0, 0), RED)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions=None):
        """Генерация случайной позиции, не занятой змейкой."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_pos = (x, y)
            if snake_positions is None or new_pos not in snake_positions:
                self.position = new_pos
                break

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки."""
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        super().__init__((start_x, start_y), GREEN)
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки с телепортацией."""
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()
        new_x = (head_x + dx * GRID_SIZE) % (GRID_WIDTH * GRID_SIZE)
        new_y = (head_y + dy * GRID_SIZE) % (GRID_HEIGHT * GRID_SIZE)
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс змейки."""
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновление направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Отрисовка змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


def handle_keys(snake):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Главный игровой цикл."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()