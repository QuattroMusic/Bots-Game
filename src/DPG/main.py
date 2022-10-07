import dearpygui.dearpygui as dpg
import src.game.variables as gv
import src.game.setup as game_setup
import src.game.update as game_update
import src.DPG.textures as DPG_textures
import src.DPG.update as DPG_update
import src.DPG.theming as DPG_theming
import src.utils as utils
from screeninfo.screeninfo import get_monitors
from threading import enumerate as thread_enumerate
from time import sleep
from src.battle.objects import Map, Vec
from src.configs import SPAWN_POS_BOT_1, SPAWN_POS_BOT_2, MAX_TROOPS
from random import shuffle
from src.game.variables import viewport_width, viewport_height


def start():
    x_pos = 100
    y_pos = 100

    for m in get_monitors():
        if m.is_primary:
            x_pos = (m.width - viewport_width) // 2
            y_pos = (m.height - viewport_height) // 2

    dpg.create_context()
    dpg.create_viewport(min_width=viewport_width, min_height=viewport_height, max_width=viewport_width, max_height=viewport_height, resizable=False, x_pos=x_pos, y_pos=y_pos)
    dpg.setup_dearpygui()

    game_setup.setup_bots()
    DPG_textures.setup_images()
    gui()
    DPG_textures.gen_terrain()
    game_setup.add_starting_troops()
    game_update.update_map_resources(gv.world_map)
    game_update.update_info_panel()
    DPG_theming.load_global_theme()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def stop_game():
    gv.is_game_running = False
    gv.waiting_to_stop_game = False
    gv.turn = 0

    while len([i for i in thread_enumerate() if i.name != "Popup"]) != 1:
        sleep(0.0001)

    dpg.set_item_label("play_button", "Play")

    for i in range(gv.resource_id + 1):
        if dpg.does_item_exist(f"resource_{i}"):
            dpg.delete_item(f"resource_{i}")

    for troop in gv.bots[0][2].troops + gv.bots[1][2].troops:
        dpg.delete_item(utils.get_troop_id(troop))
    gv.world_map = Map()

    for i in (gv.bots[0][2], gv.bots[1][2]):
        i.troops.clear()
        i.resources_pos.clear()
        i.resources = 0

    shuffle(gv.bots)
    gv.bots[0][2].spawn_pos = Vec(SPAWN_POS_BOT_1)
    gv.bots[1][2].spawn_pos = Vec(SPAWN_POS_BOT_2)

    gv.troop_id = -1
    gv.resource_id = -1

    gv.map_troop_to_id.clear()
    gv.map_resource_to_id.clear()

    game_setup.add_starting_troops()
    game_update.update_map_resources(gv.world_map)
    game_update.update_info_panel()

    gv.commands_create.clear()
    gv.commands_action.clear()
    gv.commands_powerup.clear()
    gv.commands_move.clear()

    for i, bot in enumerate(gv.bots):
        dpg.set_value(f"bot {i} text", gv.bots[i][0])


def format_slider_time(sender, data):
    data = 200 ** data
    gv.sleep_time = 1 / data
    dpg.configure_item(sender, format=f"Speed: x{round(data, 2)}")


def gen_empty_table(tag):
    with dpg.table(borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True,
                   row_background=True, tag=tag):
        for text in ["Pos", "HP", "DMG", "Speed"]:
            dpg.add_table_column(label=text)
        for _ in range(MAX_TROOPS):
            with dpg.table_row():
                for i in range(4):
                    dpg.add_text()


def gui():
    with dpg.window():
        dpg.set_primary_window(dpg.last_item(), True)
        with dpg.group(horizontal=True):
            with dpg.group():
                with dpg.child_window(height=200, width=540):
                    # game control
                    with dpg.group(horizontal=True, horizontal_spacing=60):
                        dpg.add_button(label="Stop", height=40, width=60, callback=stop_game)
                        dpg.add_button(label="Play", height=40, width=60, callback=DPG_update.play_continuous, tag="play_button")
                        dpg.add_button(label="Single Step", height=40, width=120, callback=lambda: DPG_update.next_step(True))
                    dpg.add_spacer(height=15)
                    dpg.add_text("Game Speed")
                    dpg.add_slider_float(width=400, min_value=0, default_value=0.207253, max_value=1, callback=format_slider_time, format=f"Speed: x{round(200 ** 0.207253, 2)}")
                    dpg.add_spacer(height=10)
                    dpg.add_text("Turn: 0", tag="turn_text")
                with dpg.group(horizontal=True):
                    # bots info
                    with dpg.child_window(width=266):
                        dpg.add_text(gv.bots[0][0], tag="bot 0 text", color=(0, 152, 220))
                        dpg.add_spacer(height=15)
                        dpg.add_text("Resources: 0", tag="resources_bot0")
                        dpg.add_spacer(height=15)
                        gen_empty_table("table_bot0")
                    with dpg.child_window(width=266):
                        dpg.add_text(gv.bots[1][0], tag="bot 1 text", color=(234, 50, 60))
                        dpg.add_spacer(height=15)
                        dpg.add_text("Resources: 0", tag="resources_bot1")
                        dpg.add_spacer(height=15)
                        gen_empty_table("table_bot1")
            # main game, right panel
            with dpg.child_window(tag="child_window_main_game"):
                dpg.add_drawlist(height=600, width=600, tag="drawlist")
