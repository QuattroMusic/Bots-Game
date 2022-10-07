from src.configs import MAX_TURNS
import dearpygui.dearpygui as dpg
from threading import Thread
from src.battle.objects import Resource, Map
from time import sleep
import src.game.variables as gv
import src.objects_functions as obj_func
import src.game.update as game_update
from src.DPG.animations import win_popup


def next_step(is_single_step=False):
    if gv.waiting_to_stop_game:
        return

    if is_single_step and gv.is_game_running or gv.turn >= 1000:
        # don't do a single step if the game is already running
        return

    gv.turn += 1

    # set variables in the bots
    resources_pos: list[Resource] = []
    for row in gv.world_map.map:
        for cell in row:
            if isinstance(cell, Resource):
                resources_pos.append(cell)

    for idx, bot in enumerate(gv.bots):
        # set resource pos
        bot[2].resources_pos = resources_pos.copy()
        # set enemy pos
        enemies = [i for i in gv.bots[1 - idx][2].troops]
        bot[2].enemies = enemies

        # anti-cheating system
        old_troops = [i[2].troops.copy() for i in gv.bots]
        old_enemies = [i[2].enemies.copy() for i in gv.bots]
        old_resources_pos = [i[2].resources_pos.copy() for i in gv.bots]
        old_resources = [i[2].resources for i in gv.bots]
        old_spawn_pos = [i[2].spawn_pos for i in gv.bots]

        # execute next turn
        bot[1](bot[2])

        # anti-cheating system
        for i in range(2):
            gv.bots[i][2].troops = old_troops[i].copy()
            gv.bots[i][2].enemies = old_enemies[i].copy()
            gv.bots[i][2].resources_pos = old_resources_pos[i].copy()
            gv.bots[i][2].resources = old_resources[i]
            gv.bots[i][2].spawn_pos = old_spawn_pos[i]

    # calculate commands
    next_frame: Map = obj_func.copy(gv.world_map)
    game_update.compute_movements(next_frame)
    game_update.compute_actions(next_frame)
    game_update.compute_powerup()
    game_update.compute_create(next_frame)
    game_update.update_map_resources(next_frame)
    gv.world_map = obj_func.copy(next_frame)

    # clear previous commands
    gv.commands_move.clear()
    gv.commands_action.clear()
    gv.commands_powerup.clear()
    gv.commands_create.clear()

    game_update.update_info_panel()

    if any([len(gv.bots[i][2].troops) == 0 for i in range(2)]):
        win_conditions()
        return

    if not is_single_step:
        if gv.sleep_time != 0.005:
            sleep(gv.sleep_time)


def play_continuous(sender):
    def run():
        while gv.turn < MAX_TURNS and gv.is_game_running:
            next_step()

        # when game ends
        if gv.turn == MAX_TURNS:
            dpg.set_item_label("play_button", "Play")
            win_conditions()

    if gv.waiting_to_stop_game:
        return

    gv.is_game_running = True

    if dpg.get_item_label(sender) == "Play" and gv.turn < MAX_TURNS:
        Thread(target=run, daemon=True).start()
        dpg.set_item_label(sender, "Pause")
    else:
        dpg.set_item_label(sender, "Play")
        gv.is_game_running = False


def win_conditions():
    if gv.bots[0][2].resources == gv.bots[1][2].resources or all([len(gv.bots[i][2].troops) == 0 for i in range(2)]):
        Thread(target=win_popup, args=(None,), daemon=True, name="Popup").start()
    elif (gv.bots[0][2].resources > gv.bots[1][2].resources) or (len(gv.bots[1][2].troops) == 0):
        Thread(target=win_popup, args=(gv.bots[0][0],), daemon=True, name="Popup").start()
    elif (gv.bots[0][2].resources < gv.bots[1][2].resources) or (len(gv.bots[0][2].troops) == 0):
        Thread(target=win_popup, args=(gv.bots[1][0],), daemon=True, name="Popup").start()

    gv.is_game_running = False
    gv.waiting_to_stop_game = True
    dpg.set_item_label("play_button", "Play")
