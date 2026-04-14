"""Геометрические фигуры для Тетриса - 7 типов с поворотами"""

# Формы фигур (матрицы)
SHAPES = {
    'I': {
        'color': (0, 255, 255),  # Циан
        'rotations': [
            [[1, 1, 1, 1]],
            [[1], [1], [1], [1]]
        ]
    },
    'O': {
        'color': (255, 255, 0),  # Желтый
        'rotations': [
            [[1, 1],
             [1, 1]]
        ]
    },
    'T': {
        'color': (128, 0, 128),  # Пурпурный
        'rotations': [
            [[0, 1, 0],
             [1, 1, 1]],
            [[1, 0],
             [1, 1],
             [1, 0]],
            [[1, 1, 1],
             [0, 1, 0]],
            [[0, 1],
             [1, 1],
             [0, 1]]
        ]
    },
    'S': {
        'color': (0, 255, 0),  # Зеленый
        'rotations': [
            [[0, 1, 1],
             [1, 1, 0]],
            [[1, 0],
             [1, 1],
             [0, 1]]
        ]
    },
    'Z': {
        'color': (255, 0, 0),  # Красный
        'rotations': [
            [[1, 1, 0],
             [0, 1, 1]],
            [[0, 1],
             [1, 1],
             [1, 0]]
        ]
    },
    'J': {
        'color': (0, 0, 255),  # Синий
        'rotations': [
            [[1, 0, 0],
             [1, 1, 1]],
            [[1, 1],
             [1, 0],
             [1, 0]],
            [[1, 1, 1],
             [0, 0, 1]],
            [[0, 1],
             [0, 1],
             [1, 1]]
        ]
    },
    'L': {
        'color': (255, 165, 0),  # Оранжевый
        'rotations': [
            [[0, 0, 1],
             [1, 1, 1]],
            [[1, 0],
             [1, 0],
             [1, 1]],
            [[1, 1, 1],
             [1, 0, 0]],
            [[1, 1],
             [0, 1],
             [0, 1]]
        ]
    }
}


class Tetromino:
    """Класс фигуры"""

    def __init__(self, shape_type, x, y):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.shape_data = SHAPES[shape_type]
        self.color = self.shape_data['color']
        self.rotations = self.shape_data['rotations']
        self.matrix = self.rotations[self.rotation]

    def rotate(self):
        """Поворот фигуры"""
        new_rotation = (self.rotation + 1) % len(self.rotations)
        new_matrix = self.rotations[new_rotation]
        return new_matrix

    def apply_rotation(self):
        """Применение поворота"""
        self.rotation = (self.rotation + 1) % len(self.rotations)
        self.matrix = self.rotations[self.rotation]

    def get_width(self):
        """Получение ширины фигуры"""
        return len(self.matrix[0])

    def get_height(self):
        """Получение высоты фигуры"""
        return len(self.matrix)

    @staticmethod
    def get_random_shape(x, y):
        """Получение случайной фигуры"""
        import random
        shape_type = random.choice(list(SHAPES.keys()))
        return Tetromino(shape_type, x, y)