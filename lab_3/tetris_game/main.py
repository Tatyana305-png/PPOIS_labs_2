"""
Тетрис - Лабораторная работа №3
Событийно-ориентированное программирование
Вариант 12: Тетрис с поворотами фигур
"""

import pygame
import sys
import os
from menu import Menu
from game import TetrisGame
from config_manager import ConfigManager


def main():
    """Главная функция запуска игры"""
    try:
        pygame.init()

        os.makedirs('assets/sounds', exist_ok=True)
        os.makedirs('assets/music', exist_ok=True)

        config_manager = ConfigManager('config.json')

        screen_width = 800
        screen_height = 700

        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Тетрис - Лабораторная работа №3")

        clock = pygame.time.Clock()

        while True:
            menu = Menu(screen, clock, config_manager)
            action = menu.run()

            if action == 'start':
                game = TetrisGame(screen, clock, config_manager)
                game.run()
                continue
            elif action == 'exit':
                break

        pygame.quit()
        sys.exit()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()