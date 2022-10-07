from random import shuffle
from os import listdir
import src.game.variables as gv
from src.battle.objects import Bot, Troop, Vec
from src.objects_functions import set_cell
import dearpygui.dearpygui as dpg
from src.configs import SPAWN_POS_BOT_1, SPAWN_POS_BOT_2
from src.utils import gen_troop_id


def add_starting_troops():
    for idx, i in enumerate(zip([Vec(SPAWN_POS_BOT_1), Vec(SPAWN_POS_BOT_2)], [gv.tex_troop_blue, gv.tex_troop_red], [gv.bots[0][2], gv.bots[1][2]])):
        t = Troop()
        troop_id = gen_troop_id()
        gv.map_troop_to_id.update({t: troop_id})
        t.position = i[0]
        t.owner = i[2]
        gv.bots[idx][2].troops.append(t)

        set_cell(gv.world_map, i[0], t)
        dpg.add_image(i[1], pos=(Vec((i[0].x, 10 - i[0].x)) * 64 + Vec((8, 8))).pos, parent="child_window_main_game", tag=troop_id)


def setup_bots():
    bots_path = [i for i in listdir() if i.startswith('bot_')]
    mod = lambda n: __import__(f"{bots_path[n][0:-3]}", fromlist=['object'])
    for i in range(2):
        gv.bots[i] = (bots_path[i][3:-3].replace("_", " ").title().strip(), mod(i).on_start_turn, Bot())
    shuffle(gv.bots)
    gv.bots[0][2].spawn_pos = Vec(SPAWN_POS_BOT_1)
    gv.bots[1][2].spawn_pos = Vec(SPAWN_POS_BOT_2)
