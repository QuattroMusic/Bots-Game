import dearpygui.dearpygui as dpg


def load_global_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component():
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)

    dpg.bind_theme(global_theme)
