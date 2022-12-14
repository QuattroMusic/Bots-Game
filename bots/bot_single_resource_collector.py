from src.battle.functions import move, action, powerup, create_troop, get_info
from src.battle.objects import Vec, Bot, Troop, Resource
from src.battle.constants import Stat, Direction


def on_start_turn(self: Bot):
    for troop in self.troops:
        # find closest resource
        closest_res: Vec | None = None
        closest_dist: float | None = None

        for res in self.resources_pos:
            if closest_res is None:
                closest_res = res.position
                closest_dist = (troop.position - res.position).length()

            dist = (troop.position - res.position).length()
            if dist < closest_dist:
                closest_dist = dist
                closest_res = res.position

        # if the distance is 1, do the action, else, move the bot towards the resource
        match (closest_res - troop.position).pos:
            case (x, 0) if abs(x) == 1:
                action(troop, "right" if x == 1 else "left")
            case (0, y) if abs(y) == 1:
                action(troop, "up" if y == 1 else "down")
            case (x, _) if x != 0:
                move(troop, "right" if x > 0 else "left", troop.move_speed)
            case (_, y) if y != 0:
                move(troop, "up" if y > 0 else "down", troop.move_speed)
