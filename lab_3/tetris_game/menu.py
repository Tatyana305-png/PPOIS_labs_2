"""Меню игры, таблица рекордов, справка"""

import pygame
import sys
import os


class Menu:
    """Класс меню игры"""

    def __init__(self, screen, clock, config_manager):
        self.screen = screen
        self.clock = clock
        self.config_manager = config_manager
        self.font_title = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        self.menu_items = ["Start Game", "High Scores", "Help", "Exit"]
        self.selected_index = 0
        self.running = True

        # Загрузка фонового изображения
        self.background = self.load_background()

    def load_background(self):
        """Загрузка фонового изображения"""
        try:
            bg_path = os.path.join('assets', 'background.jpg')
            if os.path.exists(bg_path):
                bg = pygame.image.load(bg_path)
                bg = pygame.transform.scale(bg, (self.screen.get_width(), self.screen.get_height()))
                return bg
            else:
                return self.create_gradient_background()
        except Exception as e:
            print(f"Не удалось загрузить фон: {e}")
            return self.create_gradient_background()

    def create_gradient_background(self):
        """Создание градиентного фона (если нет изображения)"""
        bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        for y in range(self.screen.get_height()):
            color_value = int(50 - (y / self.screen.get_height()) * 50)
            color = (0, 0, max(0, color_value))
            pygame.draw.line(bg, color, (0, y), (self.screen.get_width(), y))

        import random
        for _ in range(100):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            pygame.draw.circle(bg, (255, 255, 255), (x, y), 1)

        return bg

    def run(self):
        """Запуск меню"""
        while self.running:
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                    elif event.key == pygame.K_RETURN:
                        result = self.handle_selection()
                        if result:
                            return result
        return 'exit'

    def draw_menu(self):
        """Отрисовка меню"""
        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title_shadow = self.font_title.render("TETRIS", True, (100, 100, 0))
        title_shadow_rect = title_shadow.get_rect(center=(self.screen.get_width() // 2 + 3, 103))
        self.screen.blit(title_shadow, title_shadow_rect)

        title = self.font_title.render("TETRIS", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Lab Work #3 - Event Driven Programming", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen.get_width() // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)

        y_offset = 280

        for i, item in enumerate(self.menu_items):
            if i == self.selected_index:
                color = (255, 255, 0)
                text = self.font.render("> " + item, True, color)
                glow = self.font.render("> " + item, True, (255, 200, 0))
                glow_rect = glow.get_rect(center=(self.screen.get_width() // 2, y_offset + i * 70))
                self.screen.blit(glow, glow_rect)
            else:
                color = (180, 180, 180)
                text = self.font.render("- " + item, True, color)

            rect = text.get_rect(center=(self.screen.get_width() // 2, y_offset + i * 70))
            self.screen.blit(text, rect)

        controls = self.font_small.render("Use UP/DOWN arrows and ENTER",
                                          True, (150, 150, 150))
        controls_rect = controls.get_rect(center=(self.screen.get_width() // 2,
                                                   self.screen.get_height() - 50))
        self.screen.blit(controls, controls_rect)

    def handle_selection(self):
        """Обработка выбора пункта меню"""
        if self.selected_index == 0:
            return 'start'
        elif self.selected_index == 1:
            self.show_scores()
            return None
        elif self.selected_index == 2:
            self.show_help()
            return None
        elif self.selected_index == 3:
            return 'exit'
        return None

    def show_scores(self):
        """Отображение таблицы рекордов"""
        scores = self.config_manager.scores
        waiting = True

        while waiting:
            self.screen.blit(self.background, (0, 0))

            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            title = self.font_title.render("HIGH SCORES", True, (255, 255, 0))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(title, title_rect)

            headers = ["#", "Name", "Score", "Level", "Lines"]
            x_positions = [100, 200, 400, 550, 650]

            for i, header in enumerate(headers):
                text = self.font.render(header, True, (255, 255, 0))
                self.screen.blit(text, (x_positions[i], 120))

            pygame.draw.line(self.screen, (100, 100, 100), (50, 160), (750, 160), 2)

            y = 190
            if not scores:
                no_scores = self.font.render("No scores yet!", True, (200, 200, 200))
                no_scores_rect = no_scores.get_rect(center=(self.screen.get_width() // 2, y))
                self.screen.blit(no_scores, no_scores_rect)
            else:
                for i, score in enumerate(scores[:10]):
                    if i == 0:
                        color = (255, 215, 0)
                    elif i == 1:
                        color = (192, 192, 192)
                    elif i == 2:
                        color = (205, 127, 50)
                    else:
                        color = (255, 255, 255)

                    text = self.font_small.render(str(i + 1), True, color)
                    self.screen.blit(text, (x_positions[0], y))

                    text = self.font_small.render(score['name'], True, color)
                    self.screen.blit(text, (x_positions[1], y))

                    text = self.font_small.render(str(score['score']), True, color)
                    self.screen.blit(text, (x_positions[2], y))

                    text = self.font_small.render(str(score['level']), True, color)
                    self.screen.blit(text, (x_positions[3], y))

                    text = self.font_small.render(str(score['lines']), True, color)
                    self.screen.blit(text, (x_positions[4], y))

                    y += 40

            back_text = self.font_small.render("Press ESC or ENTER to return to menu",
                                               True, (150, 150, 150))
            back_rect = back_text.get_rect(center=(self.screen.get_width() // 2,
                                                    self.screen.get_height() - 50))
            self.screen.blit(back_text, back_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        waiting = False
                        break

    def show_help(self):
        """Отображение справки"""
        help_text = [
            "TETRIS GAME RULES",
            "",
            "Goal: Score points by completing horizontal lines",
            "",
            "Controls:",
            "Left/Right Arrow - Move piece",
            "Up Arrow - Rotate piece",
            "Down Arrow - Speed up fall",
            "Space Bar - Instant drop",
            "P - Pause game",
            "",
            "Scoring:",
            "1 line = 100 points x level",
            "2 lines = 300 points x level",
            "3 lines = 500 points x level",
            "4 lines = 800 points x level (TETRIS!)",
            "",
            "Level increases every 10 cleared lines",
            "",
            "Game ends when pieces reach the top"
        ]

        scroll_y = 0
        waiting = True

        while waiting:
            self.screen.blit(self.background, (0, 0))

            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            y = 50 - scroll_y
            for line in help_text:
                if line == "":
                    y += 15
                    continue

                if line == "TETRIS GAME RULES":
                    font = self.font_title
                    color = (255, 255, 0)
                elif line == "Goal:" or line == "Controls:" or line == "Scoring:":
                    font = self.font
                    color = (255, 255, 0)
                elif line.startswith("Left") or line.startswith("Up") or line.startswith("Down"):
                    font = self.font_small
                    color = (200, 200, 0)
                else:
                    font = self.font_small
                    color = (255, 255, 255)

                text = font.render(line, True, color)
                self.screen.blit(text, (50, y))
                y += 35

            scroll_text = self.font_small.render("UP/DOWN - scroll | ESC or ENTER - back to menu",
                                                 True, (150, 150, 150))
            scroll_rect = scroll_text.get_rect(center=(self.screen.get_width() // 2,
                                                        self.screen.get_height() - 30))
            self.screen.blit(scroll_text, scroll_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_UP:
                        scroll_y = max(0, scroll_y - 30)
                    elif event.key == pygame.K_DOWN:
                        scroll_y = min(300, scroll_y + 30)