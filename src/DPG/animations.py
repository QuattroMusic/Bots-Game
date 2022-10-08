import dearpygui.dearpygui as dpg
from src.battle.objects import Troop, Vec
import src.game.variables as gv
from time import sleep
from src.utils import get_troop_id
from src.game.variables import viewport_height, viewport_width


def move_troop_animation(troop: Troop, direction: Vec, amount: int):
    try:
        troop_id = get_troop_id(troop)
        start = Vec(((troop.position.x - direction.x * amount) * 64 + 8, (10 - (troop.position.y - direction.y * amount)) * 64 + 8))
        dpg.set_item_pos(troop_id, start.pos)

        direction = Vec((direction.x, -direction.y))
        end = Vec(dpg.get_item_pos(troop_id)) + direction * 64 * amount
        current_turn = gv.turn

        # going forward
        while gv.turn == current_turn and list(end.pos) != dpg.get_item_pos(troop_id):
            distance = end - Vec(dpg.get_item_pos(troop_id))

            step = Vec(dpg.get_item_pos(troop_id)) + Vec([distance.x // 4, distance.y // 4]) + direction
            dpg.set_item_pos(troop_id, step.pos)

            sleep(dpg.get_delta_time() / 1.3)

        pos = Vec((troop.position.x * 64 + 8, (10 - troop.position.y) * 64 + 8))
        while list(pos.pos) != dpg.get_item_pos(troop_id):
            dpg.set_item_pos(troop_id, pos.pos)
    except:
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
        while current_turn == gv.turn and list(end.pos) != dpg.get_item_pos(troop_id):
            distance = end - Vec(dpg.get_item_pos(troop_id))

            step = Vec(dpg.get_item_pos(troop_id)) + Vec([distance.x // 3, distance.y // 3]) + direction
            dpg.set_item_pos(troop_id, step.pos)

            sleep(dpg.get_delta_time() / 1.3)

        end = Vec(dpg.get_item_pos(troop_id)) - direction * 16

        # return to original position
        while current_turn == gv.turn and list(end.pos) != dpg.get_item_pos(troop_id):
            distance = end - Vec(dpg.get_item_pos(troop_id))

            step = Vec(dpg.get_item_pos(troop_id)) + Vec([distance.x // 3, distance.y // 3]) - direction
            dpg.set_item_pos(troop_id, step.pos)

            sleep(dpg.get_delta_time() / 1.3)

        pos = Vec((troop.position.x * 64 + 8, (10 - troop.position.y) * 64 + 8))
        while list(pos.pos) != dpg.get_item_pos(troop_id):
            dpg.set_item_pos(troop_id, pos.pos)
    except:
        pass


def win_popup(winner: str | None):
    # setup winner
    if winner is None:
        winner = "Draw!"
    else:
        winner = f"{winner} Won!"

    # show popup window and make a fancy animation
    popup_width = 700
    popup_height = 600
    with dpg.window(width=popup_width, height=popup_height, pos=[(viewport_width - popup_width) // 2 + 266, (viewport_height - popup_height) // 2],
                    modal=True, no_resize=True, no_collapse=True, no_scrollbar=True, no_move=True, no_title_bar=True) as popup:
        dpg.add_text(winner)
        dpg.add_spacer(height=10)
        with dpg.child_window(height=popup_height - 100):
            with dpg.table() as table:
                for i in range(2):
                    dpg.add_table_column(label=gv.bots[i][0])
                with dpg.table_row():
                    for i in range(2):
                        with dpg.plot(width=-1, height=200, no_menus=True, no_box_select=True, anti_aliased=True, pan_button=-1):
                            # resource trend
                            dpg.add_plot_axis(0, label="Turns")
                            with dpg.plot_axis(1, label="Resources"):
                                dpg.add_line_series([], [])
                with dpg.table_row():
                    dpg.add_group()
                    dpg.add_group()
        continue_button = dpg.add_button(label="Continue", width=80, height=40, callback=lambda: dpg.delete_item(popup), show=False)

    # plot animation for resource trend
    sleep(0.2)
    plots = dpg.get_item_children(dpg.get_item_children(table, 1)[0], 1)
    lines = [dpg.get_item_children(dpg.get_item_children(plot, 1)[1], 1)[0] for plot in plots]
    length_list = len(list(gv.stat_bots_resources_trend.values())[0])
    for y1, y2 in zip(list(gv.stat_bots_resources_trend.values())[0], list(gv.stat_bots_resources_trend.values())[1]):
        for plot, line, val in zip(plots, lines, [y1, y2]):
            dpg.set_value(line, [list(range(len(dpg.get_value(line)[1]))), dpg.get_value(line)[1] + [val], [], [], []])
            dpg.set_axis_limits(dpg.get_item_children(plot, 1)[0], 0, len(dpg.get_value(line)[0]) - 1)
            dpg.set_axis_limits(dpg.get_item_children(plot, 1)[1], 0, max(dpg.get_value(line)[1]))

        if length_list <= 300:
            sleep(0.01)
        elif 300 < length_list < 600:
            sleep(0.01)

    # shows bots statistics
    sleep(0.2)
    for parent, bot in zip(dpg.get_item_children(dpg.get_item_children(table, 1)[1], 1), [gv.bots[0][2], gv.bots[1][2]]):
        # put all items inside the child windows, instead of continuing setting the parent for each item
        dpg.push_container_stack(parent)
        dpg.add_text("Statistics")
        sleep(0.02)
        dpg.add_spacer(height=10)
        dpg.add_text(f"Created Troops: {gv.stat_bots_created_troops[bot]}")
        sleep(0.02)
        dpg.add_text(f"Eliminated Troops: {gv.stat_bots_eliminated_troops[bot]}")
        sleep(0.02)
        dpg.add_text(f"Eliminated Resources: {gv.stat_bots_eliminated_resources[bot]}")
        sleep(0.02)
        dpg.add_text(f"Used Resources For")
        sleep(0.02)
        dpg.add_text(f"Troops: {gv.stat_bots_used_resources[bot]['troops']}", bullet=True)
        sleep(0.02)
        dpg.add_text(f"Powerups: {gv.stat_bots_used_resources[bot]['powerup']}", bullet=True)
        sleep(0.02)
        dpg.add_spacer(height=10)

        dpg.add_text("Top 3 Attacker Troops")
        arr: list[tuple[Troop, int]] = list(gv.stat_bots_troops_kills[bot].items())
        arr.sort(key=lambda n: n[1], reverse=True)
        dpg.add_text(f"{gv.map_troop_to_id[arr[0][0]].replace('_', ' ').title()}: {arr[0][1]} Troop Killed", bullet=True)
        dpg.add_text(f"{gv.map_troop_to_id[arr[1][0]].replace('_', ' ').title()}: {arr[1][1]} Troop Killed", bullet=True)
        dpg.add_text(f"{gv.map_troop_to_id[arr[2][0]].replace('_', ' ').title()}: {arr[2][1]} Troop Killed", bullet=True)

        sleep(0.02)
        dpg.add_spacer(height=10)
        dpg.add_text("Top 3 Gatherer Troops")
        arr: list[tuple[Troop, int]] = list(gv.stat_bots_troops_resources[bot].items())
        arr.sort(key=lambda n: n[1], reverse=True)
        dpg.add_text(f"{gv.map_troop_to_id[arr[0][0]].replace('_', ' ').title()}: {arr[0][1]} Resources Destroyed", bullet=True)
        dpg.add_text(f"{gv.map_troop_to_id[arr[1][0]].replace('_', ' ').title()}: {arr[1][1]} Resources Destroyed", bullet=True)
        dpg.add_text(f"{gv.map_troop_to_id[arr[2][0]].replace('_', ' ').title()}: {arr[2][1]} Resources Destroyed", bullet=True)

        dpg.pop_container_stack()

    sleep(0.2)
    dpg.show_item(continue_button)
