import dearpygui.dearpygui as dpg
from src.battle.objects import Map, Troop, Vec, Resource
from src.objects_functions import is_outside, get_cell, set_cell
import src.game.variables as gv
from threading import Thread
from src.DPG.animations import move_troop_animation, action_troop_animation
from src.configs import GAIN_PER_RESOURCE, TROOP_POWERUP_COST, TROOP_CREATION_COST, MAX_TROOPS, MAX_RESOURCES, MAP_HEIGHT, MAP_WIDTH
from src.utils import gen_troop_id, gen_resource_id, get_troop_id, get_resource_id
from random import sample, seed
from time import time
from src.battle.constants import Stat


def compute_movements(next_frame: Map):
    valid_commands: list[list[Troop, Vec, int]] = []
    ids_found: list[str] = []
    for troop, vec, amount in gv.commands_move:
        if get_troop_id(troop) not in ids_found:
            ids_found.append(get_troop_id(troop))
            valid_commands.append([troop, vec, amount])

    done_movements: dict[Troop, tuple[Vec, int]] = {}

    valid_commands.reverse()
    while len(valid_commands) > 0:
        for i in range(len(valid_commands))[::-1]:
            troop: Troop
            movement: Vec
            amount: int
            troop, movement, amount = valid_commands[i]

            amount = max(0, min(amount, troop.move_speed))
            if amount == 0:
                valid_commands.pop(i)
                continue

            target_pos: Vec = troop.position + movement
            if is_outside(next_frame, target_pos):
                valid_commands.pop(i)
                continue
            target_cell = get_cell(next_frame, target_pos)

            if isinstance(target_cell, Resource) or isinstance(target_cell, Troop):
                valid_commands.pop(i)
                continue

            set_cell(next_frame, troop.position, None)
            set_cell(next_frame, target_pos, troop)
            troop.position = target_pos
            valid_commands[i] = [troop, movement, amount - 1]

            if troop not in done_movements:
                done_movements[troop] = (movement, 1)
            else:
                done_movements[troop] = (done_movements[troop][0], done_movements[troop][1] + 1)

    for troop, action in done_movements.items():
        Thread(target=move_troop_animation, args=(troop, action[0], action[1]), daemon=True).start()


def compute_actions(next_frame: Map):
    resources_hit_by: dict[Resource, list[Troop] | None] = {}
    troops_hit_by: dict[Troop, list[Troop] | None] = {}

    troop_has_hit: dict[Troop, bool] = {}

    for troop, _ in gv.commands_action:
        troop_has_hit.update({troop: False})

    for troop, movement in gv.commands_action:
        target_pos = troop.position + movement
        target_cell = get_cell(next_frame, target_pos)

        if troop_has_hit[troop] is False:
            troop_has_hit[troop] = True

            if isinstance(target_cell, Troop):
                target_cell.health -= troop.damage
                if target_cell in troops_hit_by:
                    troops_hit_by[target_cell].append(troop)
                else:
                    troops_hit_by[target_cell] = [troop]

            elif isinstance(target_cell, Resource):
                target_cell.health -= troop.damage
                if target_cell in resources_hit_by:
                    resources_hit_by[target_cell].append(troop)
                else:
                    resources_hit_by[target_cell] = [troop]

            Thread(target=action_troop_animation, args=(troop, movement), daemon=True).start()

    # remove troops
    for troop, attackers in troops_hit_by.items():
        if troop.health <= 0:
            # delete troop
            dpg.delete_item(get_troop_id(troop))
            set_cell(next_frame, troop.position, None)
            troop.owner.troops.remove(troop)

            # update statistics
            gv.stat_bots_eliminated_troops[attackers[0].owner] += 1
            for attacker in attackers:
                gv.stat_bots_troops_kills[attacker.owner][attacker] += 1

    # remove resources
    for resource, attackers in resources_hit_by.items():
        if resource.health <= 0:
            # destroy resource object and set resources to the bot
            dpg.delete_item(get_resource_id(resource))
            set_cell(next_frame, resource.position, None)

            for attacker in attackers:
                attacker.owner.resources += round(GAIN_PER_RESOURCE / len(attackers), 2)
                # statistics
                gv.stat_bots_eliminated_resources[attacker.owner] += 1
                gv.stat_bots_troops_resources[attacker.owner][attacker] += 1


def compute_powerup():
    for troop, power_id in gv.commands_powerup:
        if troop.owner.resources < TROOP_POWERUP_COST:
            continue

        match power_id:
            case "health" | Stat.HEALTH:
                troop.health += 1
            case "speed" | Stat.SPEED:
                troop.move_speed += 1
            case "damage" | Stat.DAMAGE:
                troop.damage += 1

        troop.owner.resources -= TROOP_POWERUP_COST

        # statistics
        gv.stat_bots_used_resources[troop.owner]['powerup'] += TROOP_POWERUP_COST


def compute_create(next_frame):
    for bot in gv.commands_create:
        if bot.resources >= TROOP_CREATION_COST and get_cell(next_frame, bot.spawn_pos) is None and len(bot.troops) < MAX_TROOPS:
            troop = Troop()
            troop_id = gen_troop_id()
            gv.map_troop_to_id.update({troop: troop_id})
            troop.position = bot.spawn_pos
            troop.owner = bot
            bot.troops.append(troop)
            set_cell(next_frame, bot.spawn_pos, troop)
            bot.resources -= TROOP_CREATION_COST

            truePos = Vec((bot.spawn_pos.x, next_frame.height - bot.spawn_pos.y - 1))
            tex = gv.tex_troop_blue if bot == gv.bots[0][2] else gv.tex_troop_red
            dpg.add_image(tex, pos=(truePos * 64 + Vec((8, 8))).pos, parent="child_window_main_game", tag=troop_id)

            # statistics
            gv.stat_bots_troops_kills[bot][troop] = 0
            gv.stat_bots_troops_resources[bot][troop] = 0
            gv.stat_bots_created_troops[bot] += 1
            gv.stat_bots_used_resources[bot]['troops'] += TROOP_CREATION_COST


def update_map_resources(next_frame: Map = gv.world_map):
    seed(time())
    resources_count = 0
    for row in next_frame.map:
        for cell in row:
            if isinstance(cell, Resource):
                resources_count += 1

    if resources_count < MAX_RESOURCES:
        empty_spots: list[Vec] = []
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                pos: Vec = Vec((x, y))
                if get_cell(next_frame, pos) is None:
                    empty_spots.append(pos)
        chosen_spots: list[Vec] = sample(empty_spots, MAX_RESOURCES - resources_count)
        for pos in chosen_spots:
            resource = Resource()
            gv.map_resource_to_id.update({resource: gen_resource_id()})
            resource.position = pos
            set_cell(next_frame, pos, resource)

        # add resources sprites on map
        for idx, pos in enumerate(chosen_spots):
            truePos = Vec((pos.x, next_frame.height - pos.y - 1))
            dpg.add_image(gv.tex_resource, pos=(truePos * 64 + Vec((8, 8))).pos, parent="child_window_main_game", tag=get_resource_id(get_cell(next_frame, pos)))
