from enum import Enum as _Enum


class Direction(_Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"


class Stat(_Enum):
    HEALTH = "health"
    SPEED = "speed"
    DAMAGE = "damage"
