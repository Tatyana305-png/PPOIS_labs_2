"""Основная логика игры Тетрис"""

import random
import pygame
from shapes import Tetromino


class TetrisBoard:
    """Класс игрового поля"""

    def __init__(self, width, height, block_size, sound_manager=None):
        self.width = width // block_size 
        self.height = height // block_size
        self.block_size = block_size
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.sound_manager = sound_manager

        self.spawn_new_piece()

    def spawn_new_piece(self):
        """Создание новой фигуры"""
        if self.next_piece is None:
            self.next_piece = Tetromino.get_random_shape(self.width // 2 - 1, 0)

        self.current_piece = self.next_piece
        self.next_piece = Tetromino.get_random_shape(self.width // 2 - 1, 0)

        if self.collision():
            self.game_over = True

    def collision(self, x_offset=0, y_offset=0, piece=None):
        """Проверка коллизий"""
        if piece is None:
            piece = self.current_piece

        for y, row in enumerate(piece.matrix):
            for x, cell in enumerate(row):
                if cell:
                    board_x = piece.x + x + x_offset
                    board_y = piece.y + y + y_offset

                    if board_x < 0 or board_x >= self.width:
                        return True
                    if board_y >= self.height:
                        return True
                    if board_y >= 0 and board_y < self.height:
                        if self.board[board_y][board_x]:
                            return True
        return False

    def merge_piece(self):
        """Фиксация фигуры на поле"""
        for y, row in enumerate(self.current_piece.matrix):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x
                    board_y = self.current_piece.y + y
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        self.board[board_y][board_x] = self.current_piece.color

    def clear_lines(self):
        """Очистка заполненных линий и подсчет очков"""
        lines_cleared = 0
        y = self.height - 1

        while y >= 0:
            if all(self.board[y]):
                for row in range(y, 0, -1):
                    self.board[row] = self.board[row - 1][:]
                self.board[0] = [0 for _ in range(self.width)]
                lines_cleared += 1
            else:
                y -= 1

        if lines_cleared > 0:
            self.lines_cleared += lines_cleared

            if self.sound_manager:
                if lines_cleared == 4:
                    self.sound_manager.play_sound('tetris')
                else:
                    self.sound_manager.play_sound('clear')

            scoring = {
                1: 100,
                2: 300,
                3: 500,
                4: 800
            }
            self.score += scoring.get(lines_cleared, 100) * self.level

            new_level = 1 + self.lines_cleared // 10
            if new_level > self.level and self.sound_manager:
                self.sound_manager.play_sound('level_up')
            self.level = new_level

        return lines_cleared

    def move_left(self):
        """Движение влево"""
        if not self.collision(x_offset=-1):
            self.current_piece.x -= 1
            return True
        return False

    def move_right(self):
        """Движение вправо"""
        if not self.collision(x_offset=1):
            self.current_piece.x += 1
            return True
        return False

    def move_down(self):
        """Движение вниз"""
        if not self.collision(y_offset=1):
            self.current_piece.y += 1
            return True
        else:
            self.merge_piece()
            self.clear_lines()
            self.spawn_new_piece()
            return False

    def rotate_piece(self):
        """Поворот фигуры"""
        original_matrix = self.current_piece.matrix
        original_rotation = self.current_piece.rotation

        new_matrix = self.current_piece.rotate()
        self.current_piece.matrix = new_matrix

        if self.collision():
            self.current_piece.matrix = original_matrix
        else:
            self.current_piece.apply_rotation()

    def hard_drop(self):
        """Мгновенное падение фигуры"""
        while not self.collision(y_offset=1):
            self.current_piece.y += 1
        self.merge_piece()
        self.clear_lines()
        self.spawn_new_piece()

    def get_drop_position(self):
        """Получение позиции фигуры после падения"""
        y = 0
        while not self.collision(y_offset=y + 1):
            y += 1
        return y