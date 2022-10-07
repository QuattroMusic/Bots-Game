import src.objects_functions as _internal
from src.battle.objects import Troop, Vec, Resource, Bot


def move(troop: Troop, direction: str, amount: int):
    """
    Moves the troop in a given direction
    arguments
        troop: the troop to move
        direction: one of 'up', 'down', 'left' or 'right'
        amount: how many cells to move
    """
    _internal.move(troop=troop, direction=direction, amount=amount)


def action(troop: Troop, direction: str):
    """
    UNDOCUMENTED
    """
    _internal.action(troop=troop, direction=direction)


def powerup(troop: Troop, stat: str):
    """
    UNDOCUMENTED
    """
    _internal.powerup(troop=troop, stat=stat)


def create_troop(bot: Bot):
    """
    UNDOCUMENTED
    """
    _internal.create(bot=bot)


def get_info(pos: Vec) -> Troop | Resource | None:
    """
    UNDOCUMENTED
    """
    return _internal.get_info(pos)
