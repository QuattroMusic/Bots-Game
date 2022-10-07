from src.battle.objects import Map, Resource, Troop, Vec, Bot
import src.game.variables as gv
from src.utils import eval_direction


def get_cell(map_: Map, pos: Vec) -> None | Troop | Resource:
    true_cell = (map_.height - pos.y - 1, pos.x)
    return map_.map[true_cell[0]][true_cell[1]]


def set_cell(map_: Map, pos: Vec, obj: None | Resource | Troop):
    true_cell = (map_.height - pos.y - 1, pos.x)
    map_.map[true_cell[0]][true_cell[1]] = obj


def copy(map_: Map) -> Map:
    new_map = Map()
    new_map.map = [[cell for cell in row] for row in map_.map]
    return new_map


def is_outside(map_: Map, pos: Vec) -> bool:
    return pos.x < 0 or pos.x >= map_.width or pos.y < 0 or pos.y >= map_.height


def move(troop, direction: str, amount: int):
    gv.commands_move.append((troop, eval_direction(direction), amount))


def action(troop, direction: str):
    gv.commands_action.append((troop, eval_direction(direction)))


def powerup(troop, stat: str):
    gv.commands_powerup.append((troop, stat))


def create(bot: Bot):
    gv.commands_create.append(bot)


def get_info(pos: Vec):
    return get_cell(gv.world_map, pos)
