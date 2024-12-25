""" Creating text interface"""
import sys

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    """ Initializing parameters """

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height + 50))

        self.paused = False
        self.pause_button = pygame.Rect(10, self.height + 10, 50, 30)
        self.resume_button = pygame.Rect(90, self.height + 10, 50, 30)

        pygame.font.init()
        self.font = pygame.font.SysFont("Montserrat", 14)

    def draw_lines(self) -> None:
        """ Drawing lines """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(
                "gray"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(
                "gray"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """ Creating Grid """
        for x, row in enumerate(self.life.curr_generation):
            for y, cell in enumerate(row):
                color = pygame.Color(
                    "green") if cell else pygame.Color("white")
                pygame.draw.rect(
                    self.screen, color, (x * self.cell_size, y *
                                         self.cell_size, self.cell_size, self.cell_size)
                )

    def draw_console(self) -> None:
        """Отрисовывает кнопки с текстом"""
        self._draw_button(self.pause_button, "pause")
        self._draw_button(self.resume_button, "resume")
        self._draw_info()

    def _draw_button(self, button_rect, text):
        """Отрисовывает одну кнопку"""
        pygame.draw.rect(self.screen, pygame.Color(
            "light gray"), button_rect, border_radius=10)
        button_text = self.font.render(text, True, pygame.Color("black"))
        self.screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    def _draw_info(self):
        """Отрисовывает дополнительную информацию"""
        gen_text = self.font.render(
            f"Generation: {self.life.generations}", True, pygame.Color("Red"))
        exit_text = self.font.render(
            "press [q] to exit", True, pygame.Color("Blue"))
        self.screen.blit(gen_text, (self.width - 200, self.height + 10))
        self.screen.blit(exit_text, (self.width - 200, self.height + 30))

    def draw_caution(self, caut_text) -> None:
        """Отрисовывает текст предупреждения"""
        caution_text = self.font.render(
            caut_text, True, pygame.Color("Purple"))
        text_rect = caution_text.get_rect(
            center=(self.width // 2, self.height // 2))
        self.screen.blit(caution_text, text_rect)

    def run(self) -> None:
        """Запускает игру"""
        pygame.init()  # pylint: disable=no-member
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                                 event.key == pygame.K_q):  # pylint: disable=no-member
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # pylint: disable=no-member
                    self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    x, y = event.pos  # Получаем координаты мыши
                    j, i = x // self.cell_size, y // self.cell_size  # Определяем индекс клетки
                    if self.pause_button.collidepoint(x, y):
                        self.paused = True
                    elif self.resume_button.collidepoint(x, y):
                        self.paused = False
                    else:
                        # Переключаем состояние клетки
                        self.life.curr_generation[i][j] = (
                            1 if self.life.curr_generation[i][j] == 0 else 0
                        )

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            self.draw_console()
            self._check_cautions()

            pygame.display.flip()

            if not self.paused:
                self.life.step()

            clock.tick(self.speed)

        pygame.quit()  # pylint: disable=no-member
        sys.exit()

    def _check_cautions(self):
        """Проверяет условия для предупреждений"""
        if self.life.is_max_generations_exceeded:
            self.draw_caution("Max generations exceeded")
            self.paused = True
        elif not self.life.is_changing:
            self.draw_caution("No changes in generations")
            self.paused = True
