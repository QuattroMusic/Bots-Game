import src.objects_functions as _internal
from src.battle.objects import Troop, Vec, Resource, Bot


def move(troop: Troop, direction: str, amount: int):
    """
    Moves the troop in a given direction
    arguments
        troop: the troop that moves
        direction: one of 'up', 'down', 'left' or 'right'
        amount: how many cells to move
    """
    _internal.move(troop=troop, direction=direction, amount=amount)


def action(troop: Troop, direction: str):
    """
    Makes the troop attack a resource or an enemy in a given direction
    arguments
        troop: the troop that executes the action
        direction: one of 'up', 'down', 'left' or 'right'
    """
    _internal.action(troop=troop, direction=direction)


def powerup(troop: Troop, stat: str):
    """
    Powerup a single troop statistic
    arguments
        troop: the troop that gets the powerup
        stat: one of 'health', 'speed' or 'damage'
    """
    _internal.powerup(troop=troop, stat=stat)


def create_troop(bot: Bot):
    """
    Creates a new troop
    arguments:
        bot: the bot that get the new troop
    """
    _internal.create(bot=bot)


def get_info(pos: Vec) -> None | Troop | Resource:
    """
    Analyzes the given cell
    arguments:
        pos: The position of the cell. (0, 0) is bottom left
    """
    return _internal.get_info(pos)
