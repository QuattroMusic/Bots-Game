from src.battle.functions import move, action, powerup, create_troop, get_info
from src.battle.objects import Vec, Bot, Troop, Resource
from src.battle.constants import Stat, Direction


def on_start_turn(self: Bot):
    create_troop(self)

    for idx, troop in enumerate(self.troops):
        if 0 <= idx <= 2 or idx == 9:
            gatherer_role(troop, self.resources_pos)
        else:
            attacker_role(troop, self.enemies)

    if self.resources >= 100:
        for idx, troop in enumerate(self.troops):
            if troop.damage < 3:
                powerup(troop, Stat.DAMAGE)
            if troop.move_speed < 2:
                powerup(troop, Stat.SPEED)


def gatherer_role(troop: Troop, resources_pos: list[Resource]):
    # find closest resource
    closest_res: Vec | None = None
    closest_dist: float | None = None

    for res in resources_pos:
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


def attacker_role(troop: Troop, enemies: list[Troop]):
    # find closest enemy
    closest_enemy: Vec | None = None
    closest_dist: float | None = None

    for enemy in enemies:
        if closest_enemy is None:
            closest_enemy = enemy.position
            closest_dist = (troop.position - enemy.position).length()

        dist = (troop.position - enemy.position).length()
        if dist < closest_dist:
            closest_dist = dist
            closest_enemy = enemy.position

    # if the distance is 1, do the action, else, move the bot towards the enemy
    match (closest_enemy - troop.position).pos:
        case (x, 0) if abs(x) == 1:
            action(troop, "right" if x == 1 else "left")
        case (0, y) if abs(y) == 1:
            action(troop, "up" if y == 1 else "down")
        case (x, _) if x != 0:
            move(troop, "right" if x > 0 else "left", troop.move_speed)
        case (_, y) if y != 0:
            move(troop, "up" if y > 0 else "down", troop.move_speed)
