from typing import Any, Self
from abc import ABC, abstractmethod


class Price(float):
    _price_instance = None

    def __new__(cls, value: Any) -> Self:
        v = float(value)
        if cls._price_instance is None:
            cls._price_instance = super().__new__(cls, v)
            cls._price_instance.value = v
        return cls._price_instance

    def __init__(Self, value: Any) -> None:
        Price._price_instance = float(value)


# def calulate_tot_items_price(items, price: Price):
#     return items * price

# p1 = Price(10)
# p2 = Price(20)

# print(p1 is p2)


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating real connection...")
            cls._instance = super().__new__(cls)
            # real expensive initialization here (or later)
            cls._instance._conn = "expensive connection object"
        return cls._instance


# db1 = Database()
# db2 = Database()

# print(db1 is db2)


from typing import Any, Self


class Price(float):
    __instance: Self | None = None

    def __new__(cls, value: Any = 0.0):
        if cls.__instance is None:
            # Only once: real creation
            cls.__instance = super().__new__(cls)
            # Optional: set some default/internal state if needed
            cls.__instance._raw_value = 0.0

    def __init__(self, value: Any = 0.0) -> None:
        # This runs EVERY TIME someone calls Price(...)
        v = float(value)
        if v < 0:
            raise ValueError("Price cannot be negative")
        self.value = v

        print(f"Price updated/reset to: {v}")


# ──────────────────────── Test ────────────────────────

p = Price(100)

p = Price(25.5)  # ← __init__ runs again → updates the same object
# Price(25.5)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def connect(self):
        print("Connecting to database...")


# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True


from typing import Any, Self


class SingletonMeta(type):
    _instances = {}

    def __init__(cls, *args, **kwargs):
        print("SingletonMeta init called")
        super().__init__(*args, **kwargs)
        cls._instances[cls] = None

    def __call__(cls, *args, **kwargs):
        print("SingletonMeta call called")
        return cls._instances[cls]


class myclass(metaclass=SingletonMeta):
    def __init__(self):
        print("myclass init called")


class Animal(ABC):
    @abstractmethod
    def walk(cls):
        pass

    @abstractmethod
    def speak(cls):
        pass

    @abstractmethod
    def eat(cls):
        pass


class dog(Animal):
    def walk(self):
        print("Dog is walking")

    def speak(self):
        print("Bow")

    def eat(self):
        print("Dog is eating")

    def __name__(self):
        return self.__name__


def get_animal(obj: Animal):
    return obj.name


print(get_animal(dog()))
