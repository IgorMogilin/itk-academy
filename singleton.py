# 1. Метакласс


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ClassA(metaclass=SingletonMeta):
    pass

# 2. Метод __new__ (простая версия)
class ClassB:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

# 3. Механизм импортов
# module_singleton.py
class _Service:
    pass

service = _Service()

# main.py
from module_singleton import service
