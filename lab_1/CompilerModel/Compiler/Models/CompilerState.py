from enum import Enum


class CompilerState(Enum):
    """Состояния компилятора"""
    INITIALIZED = "Инициализирован"
    LEXICAL_ANALYSIS = "Лексический анализ"
    SYNTAX_ANALYSIS = "Синтаксический анализ"
    OPTIMIZATION = "Оптимизация"
    CODE_GENERATION = "Генерация кода"
    COMPLETED = "Завершено"
    ERROR = "Ошибка"

    @classmethod
    def get_all_stages(cls):
        """Возвращает все этапы компиляции по порядку"""
        return [
            cls.LEXICAL_ANALYSIS,
            cls.SYNTAX_ANALYSIS,
            cls.OPTIMIZATION,
            cls.CODE_GENERATION,
            cls.COMPLETED
        ]

    @classmethod
    def get_stage_index(cls, stage):
        """Возвращает индекс этапа"""
        stages = cls.get_all_stages()
        if stage in stages:
            return stages.index(stage)
        return -1
