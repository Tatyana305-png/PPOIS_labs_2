"""Управление конфигурационными файлами в формате JSON"""

import json
import os


class ConfigManager:
    """Класс для работы с конфигурациями"""

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()
        self.scores_file = 'scores.json'
        self.scores = self.load_scores()

    def load_config(self):
        """Загрузка конфигурации из JSON файла"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print("Файл конфигурации пуст. Создаю конфигурацию по умолчанию...")
                    return self.create_default_config()
                f.seek(0)
                return json.load(f)
        except FileNotFoundError:
            print("Файл конфигурации не найден. Создаю конфигурацию по умолчанию...")
            return self.create_default_config()
        except json.JSONDecodeError as e:
            print(f"Ошибка в JSON файле конфигурации: {e}")
            print("Создаю конфигурацию по умолчанию...")
            return self.create_default_config()

    def create_default_config(self):
        """Создание конфигурации по умолчанию"""
        default_config = {
            "game": {
                "width": 300,
                "height": 600,
                "block_size": 30,
                "fps": 60,
                "initial_speed": 500,
                "speed_increase_per_level": 50,
                "min_speed": 100
            },
            "scoring": {
                "single_line": 100,
                "double_line": 300,
                "triple_line": 500,
                "tetris_line": 800
            },
            "colors": {
                "background": [0, 0, 0],
                "grid": [40, 40, 40],
                "text": [255, 255, 255],
                "shadow": [100, 100, 100],
                "preview_bg": [20, 20, 20]
            }
        }
        self.save_config(default_config)
        return default_config

    def save_config(self, config):
        """Сохранение конфигурации в JSON файл"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении конфигурации: {e}")

    def get_config(self):
        """Получение конфигурации"""
        return self.config

    def load_scores(self):
        """Загрузка таблицы рекордов"""
        try:
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print("Файл рекордов пуст. Создаю таблицу рекордов по умолчанию...")
                    return self.create_default_scores()
                f.seek(0)
                scores = json.load(f)
                if not isinstance(scores, list):
                    print("Неверный формат файла рекордов. Создаю новую таблицу...")
                    return self.create_default_scores()
                scores.sort(key=lambda x: x['score'], reverse=True)
                return scores
        except FileNotFoundError:
            print("Файл рекордов не найден. Создаю таблицу рекордов по умолчанию...")
            return self.create_default_scores()
        except json.JSONDecodeError as e:
            print(f"Ошибка в JSON файле рекордов: {e}")
            print("Создаю таблицу рекордов по умолчанию...")
            return self.create_default_scores()

    def create_default_scores(self):
        """Создание таблицы рекордов по умолчанию"""
        default_scores = []
        self.save_scores(default_scores)
        return default_scores

    def save_scores(self, scores):
        """Сохранение таблицы рекордов"""
        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении таблицы рекордов: {e}")

    def add_score(self, name, score, level, lines):
        """Добавление нового рекорда"""
        self.scores.append({"name": name, "score": score, "level": level, "lines": lines})
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]
        self.save_scores(self.scores)
        print(f"Рекорд сохранен: {name} - {score} очков")

    def is_high_score(self, score):
        """
        Проверка, является ли результат рекордным.
        """
        if score <= 0:
            print(f"Счет {score} <= 0, не рекорд")
            return False

        if len(self.scores) == 0:
            print(f"Таблица рекордов пуста, счет {score} - рекорд!")
            return True

        if len(self.scores) < 10:
            print(f"В таблице {len(self.scores)} записей (<10), счет {score} - рекорд!")
            return True

        lowest_score = self.scores[-1]['score']
        is_high = score > lowest_score
        print(f"Самый низкий рекорд: {lowest_score}, ваш счет: {score}, рекорд: {is_high}")
        return is_high

    def get_highest_score(self):
        """Получение самого высокого рекорда"""
        if self.scores:
            return self.scores[0]['score']
        return 0