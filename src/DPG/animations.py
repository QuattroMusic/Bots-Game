import dearpygui.dearpygui as dpg
from src.battle.objects import Troop, Vec
import src.game.variables as gv
from time import sleep
from src.utils import get_troop_id
from src.game.variables import viewport_height


def move_troop_animation(troop: Troop, direction: Vec, amount: int):
    try:
        troop_id = get_troop_id(troop)
        start = Vec(((troop.position.x - direction.x * amount) * 64 + 8, (10 - (troop.position.y - direction.y * amount)) * 64 + 8))
        dpg.set_item_pos(troop_id, start.pos)

        direction = Vec((direction.x, -direction.y))
        end = Vec(dpg.get_item_pos(troop_id)) + direction * 64 * amount
        current_turn = gv.turn

        # going forward
        while gv.turn == current_turn and end.pos != dpg.get_item_pos(troop_id):
            distance = end - Vec(dpg.get_item_pos(troop_id))

            step = Vec(dpg.get_item_pos(troop_id)) + Vec([distance.x // 4, distance.y // 4]) + direction
            dpg.set_item_pos(troop_id, step.pos)

            sleep(dpg.get_delta_time() / 1.3)

        pos = Vec((troop.position.x * 64 + 8, (10 - troop.position.y) * 64 + 8))
        while pos.pos != dpg.get_item_pos(troop_id):
            dpg.set_item_pos(troop_id, pos.pos)
    except SystemError:
        pass


def action_troop_animation(troop: Troop, direction: Vec):
    try:
        troop_id = get_troop_id(troop)
        start = Vec((troop.position.x * 64 + 8, (10 - troop.position.y) * 64 + 8))
        dpg.set_item_pos(troop_id, start.pos)

        direction = Vec((direction.x, -direction.y))
        end = Vec(dpg.get_item_pos(troop_id)) + direction * 16
        current_turn = gv.turn

        # going forward a bit
        while current_turn == gv.turn and end.pos != dpg.get_item_pos(troop_id):
            distance = end - Vec(dpg.get_item_pos(troop_id))

            step = Vec(dpg.get_item_pos(troop_id)) + Vec([distance.x // 3, distance.y // 3]) + direction
            dpg.set_item_pos(troop_id, step.pos)

            sleep(dpg.get_delta_time() / 1.3)

        end = Vec(dpg.get_item_pos(troop_id)) - direction * 16

        # return to original position
        while current_turn == gv.turn and end.pos != dpg.get_item_pos(troop_id):
            distance = end - Vec(dpg.get_item_pos(troop_id))

            step = Vec(dpg.get_item_pos(troop_id)) + Vec([distance.x // 3, distance.y // 3]) - direction
            dpg.set_item_pos(troop_id, step.pos)

            sleep(dpg.get_delta_time() / 1.3)

        pos = Vec((troop.position.x * 64 + 8, (10 - troop.position.y) * 64 + 8))
        while pos.pos != dpg.get_item_pos(troop_id):
            dpg.set_item_pos(troop_id, pos.pos)
    except SystemError:
        pass


def win_popup(winner: str | None):
    # setup winner
    if winner is None:
        winner = "Draw!"
    else:
        winner = f"{winner} Win!"
    length = len(str(winner)) * 7 + 25

    # show popup window and make a fancy animation
    with dpg.window(pos=[266 - (length - 8) // 2, viewport_height], no_resize=True, no_collapse=True, no_scrollbar=True, no_close=True, no_move=True, no_title_bar=True, no_background=True) as popup:
        dpg.add_spacer(height=50)
        with dpg.child_window(height=40, width=length):
            dpg.add_text(winner)

    while dpg.get_item_pos(popup) != [266 - (length - 8) // 2, viewport_height - 150]:
        distance = Vec(dpg.get_item_pos(popup)) - Vec([266 - (length - 8) // 2, viewport_height - 150])
        dpg.set_item_pos(popup, (Vec(dpg.get_item_pos(popup)) - distance / 5).pos)
        sleep(0.02)

    sleep(2)

    dpg.delete_item(popup)
