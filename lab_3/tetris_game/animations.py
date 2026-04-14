"""Анимации для игры"""

import pygame


class Animations:
    """Класс для управления анимациями"""

    def __init__(self, screen, block_size):
        self.screen = screen
        self.block_size = block_size
        self.animations = []

    def add_line_clear_animation(self, rows, board_x, board_y):
        """Анимация очистки линий"""
        self.animations.append({
            'type': 'line_clear',
            'rows': rows,
            'x': board_x,
            'y': board_y,
            'timer': 0,
            'duration': 10
        })

    def add_piece_drop_animation(self, piece, start_y, end_y, board_x, board_y):
        """Анимация падения фигуры"""
        self.animations.append({
            'type': 'piece_drop',
            'piece': piece,
            'start_y': start_y,
            'end_y': end_y,
            'current_y': start_y,
            'x': board_x,
            'timer': 0,
            'duration': 5
        })

    def add_piece_spawn_animation(self, piece, board_x, board_y):
        """Анимация появления фигуры"""
        self.animations.append({
            'type': 'piece_spawn',
            'piece': piece,
            'x': board_x,
            'y': board_y,
            'timer': 0,
            'duration': 5,
            'alpha': 0
        })

    def update(self):
        """Обновление анимаций"""
        completed = []
        for i, anim in enumerate(self.animations):
            anim['timer'] += 1
            if anim['timer'] >= anim['duration']:
                completed.append(i)

        for i in reversed(completed):
            self.animations.pop(i)

    def draw(self):
        """Отрисовка анимаций"""
        for anim in self.animations:
            if anim['type'] == 'line_clear':
                self._draw_line_clear_animation(anim)
            elif anim['type'] == 'piece_drop':
                self._draw_piece_drop_animation(anim)
            elif anim['type'] == 'piece_spawn':
                self._draw_piece_spawn_animation(anim)

    def _draw_line_clear_animation(self, anim):
        """Отрисовка анимации очистки линий"""
        progress = anim['timer'] / anim['duration']
        alpha = 255 - int(progress * 255)

        for row in anim['rows']:
            y = anim['y'] + row * self.block_size
            rect = pygame.Rect(anim['x'], y,
                               self.block_size * 10, self.block_size)

            if progress < 0.5:
                color = (255, 255, 255, alpha)
            else:
                color = (255, 0, 0, alpha)

            s = pygame.Surface(rect.size, pygame.SRCALPHA)
            s.fill(color)
            self.screen.blit(s, rect)

    def _draw_piece_drop_animation(self, anim):
        """Отрисовка анимации падения фигуры"""
        progress = anim['timer'] / anim['duration']
        y = anim['start_y'] + (anim['end_y'] - anim['start_y']) * progress

        piece = anim['piece']
        for py, row in enumerate(piece.matrix):
            for px, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        anim['x'] + (piece.x + px) * self.block_size,
                        y + (piece.y + py) * self.block_size,
                        self.block_size - 1,
                        self.block_size - 1
                    )
                    pygame.draw.rect(self.screen, piece.color, rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

    def _draw_piece_spawn_animation(self, anim):
        """Отрисовка анимации появления фигуры"""
        progress = anim['timer'] / anim['duration']
        alpha = int(progress * 255)

        piece = anim['piece']
        for py, row in enumerate(piece.matrix):
            for px, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        anim['x'] + (piece.x + px) * self.block_size,
                        anim['y'] + (piece.y + py) * self.block_size,
                        self.block_size - 1,
                        self.block_size - 1
                    )
                    # Эффект масштабирования
                    scale = 0.5 + progress * 0.5
                    center = rect.center
                    new_rect = pygame.Rect(
                        center[0] - rect.width * scale / 2,
                        center[1] - rect.height * scale / 2,
                        rect.width * scale,
                        rect.height * scale
                    )
                    pygame.draw.rect(self.screen, piece.color, new_rect)