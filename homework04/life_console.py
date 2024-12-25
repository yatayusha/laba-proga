"""Creating console interface"""
import curses

from life import GameOfLife
from ui import UI

# Реализуем игровой процесс в текстовом интерфейсе с управлением


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        height, width = screen.getmaxyx()
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                if 0 < i < height - 1 and 0 < j < width - 1:
                    char = "O" if cell else " "
                    screen.addch(i, j, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)
        screen.timeout(100)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        running = True
        try:
            while running:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                height, _ = screen.getmaxyx()
                screen.addstr(
                    height - 1,
                    0,
                    f"Press [q] to quit | Generation: {self.life.generations}",
                    curses.color_pair(1) | curses.A_BOLD,
                )

                screen.refresh()
                self.life.step()
                key = screen.getch()
                if key == ord("q"):
                    running = False
                    break
        finally:
            curses.endwin()
            running = False
