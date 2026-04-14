"""Основной игровой цикл и обработка событий"""

import pygame
import sys
from tetris import TetrisBoard
from sounds import SoundManager


class TetrisGame:
    """Класс игры Тетрис"""

    def __init__(self, screen, clock, config_manager):
        self.screen = screen
        self.clock = clock
        self.config_manager = config_manager
        self.config = config_manager.get_config()

        self.block_size = 30

        self.sound_manager = SoundManager()

        self.board = TetrisBoard(300, 600, self.block_size, self.sound_manager)

        self.fall_time = 0
        self.fall_speed = 500
        self.paused = False
        self.running = True
        self.game_over_ready = False

        self.font_title = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.board_x = 50
        self.board_y = 80
        self.info_x = 400

        self.sound_manager.play_music()

    def run(self):
        """Основной игровой цикл"""
        while self.running:
            dt = self.clock.tick(60)

            if not self.paused and not self.board.game_over:
                self.fall_time += dt
                if self.fall_time >= self.fall_speed:
                    self.fall_time = 0
                    self.board.move_down()
                    self.fall_speed = max(100, 500 - (self.board.level - 1) * 30)

            self.handle_events()
            self.draw()
            pygame.display.flip()

        if self.board.game_over:
            self.game_over_sequence()

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if self.board.game_over:
                    if event.key == pygame.K_RETURN:
                        self.running = False
                        self.game_over_ready = True
                    return

                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    continue

                if self.paused:
                    continue

                if event.key == pygame.K_LEFT:
                    self.board.move_left()
                    self.sound_manager.play_sound('move')

                elif event.key == pygame.K_RIGHT:
                    self.board.move_right()
                    self.sound_manager.play_sound('move')

                elif event.key == pygame.K_DOWN:
                    self.board.move_down()
                    self.sound_manager.play_sound('drop')

                elif event.key == pygame.K_UP:
                    self.board.rotate_piece()
                    self.sound_manager.play_sound('rotate')

                elif event.key == pygame.K_SPACE:
                    self.board.hard_drop()
                    self.sound_manager.play_sound('drop')

    def draw(self):
        """Отрисовка игры"""
        self.screen.fill((0, 0, 0))

        title = self.font_title.render("TETRIS", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(title, title_rect)

        self.draw_board()

        if self.board.current_piece and not self.board.game_over:
            self.draw_piece()

        self.draw_info_panel()

        if self.paused:
            self.draw_pause()

        if self.board.game_over:
            self.draw_game_over()

    def draw_board(self):
        """Отрисовка игрового поля"""
        border_rect = pygame.Rect(self.board_x - 3, self.board_y - 3,
                                  10 * self.block_size + 6,
                                  20 * self.block_size + 6)
        pygame.draw.rect(self.screen, (100, 100, 100), border_rect, 3)

        for y in range(self.board.height):
            for x in range(self.board.width):
                rect = pygame.Rect(
                    self.board_x + x * self.block_size,
                    self.board_y + y * self.block_size,
                    self.block_size - 1,
                    self.block_size - 1
                )

                if self.board.board[y][x]:
                    color = self.board.board[y][x]
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                else:
                    pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def draw_piece(self):
        """Отрисовка текущей фигуры"""
        piece = self.board.current_piece
        for y, row in enumerate(piece.matrix):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        self.board_x + (piece.x + x) * self.block_size,
                        self.board_y + (piece.y + y) * self.block_size,
                        self.block_size - 1,
                        self.block_size - 1
                    )
                    pygame.draw.rect(self.screen, piece.color, rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

    def draw_info_panel(self):
        """Отрисовка информационной панели"""
        y = 80

        score_text = self.font.render(f"Score: {self.board.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.info_x, y))

        level_text = self.font.render(f"Level: {self.board.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (self.info_x, y + 50))

        lines_text = self.font.render(f"Lines: {self.board.lines_cleared}", True, (255, 255, 255))
        self.screen.blit(lines_text, (self.info_x, y + 100))

        next_title = self.font.render("Next:", True, (255, 255, 255))
        self.screen.blit(next_title, (self.info_x, y + 180))

        if self.board.next_piece:
            next_x = self.info_x + 20
            next_y = y + 220
            piece = self.board.next_piece
            for py, row in enumerate(piece.matrix):
                for px, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            next_x + px * self.block_size,
                            next_y + py * self.block_size,
                            self.block_size - 1,
                            self.block_size - 1
                        )
                        pygame.draw.rect(self.screen, piece.color, rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

        controls_y = y + 400
        controls_title = self.font_small.render("Controls:", True, (255, 255, 0))
        self.screen.blit(controls_title, (self.info_x, controls_y))

        controls = [
            "Left/Right - Move",
            "Up - Rotate",
            "Down - Speed up",
            "Space - Hard drop",
            "P - Pause"
        ]

        for i, text in enumerate(controls):
            ctrl = self.font_small.render(text, True, (180, 180, 180))
            self.screen.blit(ctrl, (self.info_x, controls_y + 30 + i * 25))

    def draw_pause(self):
        """Отрисовка паузы"""
        s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))

        pause_text = self.font.render("PAUSE", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2,
                                                  self.screen.get_height() // 2))
        self.screen.blit(pause_text, pause_rect)

        continue_text = self.font_small.render("Press P to continue", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(self.screen.get_width() // 2,
                                                        self.screen.get_height() // 2 + 50))
        self.screen.blit(continue_text, continue_rect)

    def draw_game_over(self):
        """Отрисовка Game Over"""
        s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.screen.blit(s, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2,
                                                          self.screen.get_height() // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        restart_text = self.font_small.render("Press ENTER", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2,
                                                      self.screen.get_height() // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def game_over_sequence(self):
        """Последовательность завершения игры"""
        self.sound_manager.play_sound('game_over')

        print("\n" + "=" * 50)
        print(f"ИГРА ОКОНЧЕНА!")
        print(f"Ваш счет: {self.board.score}")
        print(f"Ваш уровень: {self.board.level}")
        print(f"Очищено линий: {self.board.lines_cleared}")
        print("-" * 50)

        is_high = self.config_manager.is_high_score(self.board.score)
        print(f"Это новый рекорд? {is_high}")

        if is_high:
            print("Запрашиваем имя для сохранения рекорда...")
            self.show_high_score_dialog()
        else:
            print("Рекорд не побит. Возвращаемся в меню...")
        print("=" * 50 + "\n")

    def show_high_score_dialog(self):
        """Диалог ввода имени для рекорда"""
        name = ""
        active = True
        cursor_blink = 0

        while active:
            self.draw()

            s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            s.fill((0, 0, 0, 220))
            self.screen.blit(s, (0, 0))

            title = self.font.render("NEW HIGH SCORE!", True, (255, 255, 0))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(title, title_rect)

            score_text = self.font.render(f"Score: {self.board.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 220))
            self.screen.blit(score_text, score_rect)

            input_box = pygame.Rect(self.screen.get_width() // 2 - 150, 300, 300, 50)
            pygame.draw.rect(self.screen, (60, 60, 60), input_box)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)

            cursor_blink = (cursor_blink + 1) % 30
            display_name = name + ("_" if cursor_blink < 15 else " ")
            name_surface = self.font.render(display_name, True, (255, 255, 255))
            self.screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

            name_label = self.font_small.render("Enter your name:", True, (200, 200, 200))
            name_rect = name_label.get_rect(center=(self.screen.get_width() // 2, 280))
            self.screen.blit(name_label, name_rect)

            prompt = self.font_small.render("Press ENTER to save, ESC to cancel",
                                           True, (150, 150, 150))
            prompt_rect = prompt.get_rect(center=(self.screen.get_width() // 2, 400))
            self.screen.blit(prompt, prompt_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        self.config_manager.add_score(name, self.board.score,
                                                      self.board.level, self.board.lines_cleared)
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        active = False
                    elif len(name) < 15 and event.unicode.isprintable():
                        name += event.unicode

            self.clock.tick(30)