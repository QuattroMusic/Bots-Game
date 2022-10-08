from src.battle.objects import Troop, Resource, Vec
import src.game.variables as gv
from src.battle.constants import Direction


def eval_direction(direction: str) -> Vec:
    match direction:
        case "up" | Direction.UP:
            return Vec((0, 1))
        case "right" | Direction.RIGHT:
            return Vec((1, 0))
        case "down" | Direction.DOWN:
            return Vec((0, -1))
        case "left" | Direction.LEFT:
            return Vec((-1, 0))


def gen_troop_id() -> str:
    gv.troop_id += 1
    return f"troop_{gv.troop_id}"


def gen_resource_id() -> str:
    gv.resource_id += 1
    return f"resource_{gv.resource_id}"


def get_troop_id(troop: Troop) -> str:
    if troop in gv.map_troop_to_id:
        return gv.map_troop_to_id[troop]


def get_resource_id(resource: Resource) -> str:
    return gv.map_resource_to_id[resource]
