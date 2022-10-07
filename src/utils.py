from src.battle.objects import Troop, Resource, Vec
import src.game.variables as gv


def eval_direction(direction: str) -> Vec:
    match direction:
        case "up":
            return Vec((0, 1))
        case "right":
            return Vec((1, 0))
        case "down":
            return Vec((0, -1))
        case "left":
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
