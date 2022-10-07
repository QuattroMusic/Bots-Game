from src.battle.functions import *
from src.battle.objects import *
from random import random


def on_start_turn(self: Bot):
    if 0.2 < random() < 0.3:
        create_troop(self)
    for troop in self.troops:
        if random() <= 0.2:
            continue
        # find closest resource
        closest_res = None
        closest_dist = None

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
