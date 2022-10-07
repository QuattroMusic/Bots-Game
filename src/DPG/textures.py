import dearpygui.dearpygui as dpg
from src.configs import MAP_WIDTH, MAP_HEIGHT
from src.battle.objects import Vec
import src.game.variables as gv


def setup_images():
    def stretch_image(data, width: int, height: int, stretch: int) -> tuple[int, int, list[int]]:
        res = [0 for _ in range(width * height * 4 * stretch * stretch)]
        dataValues = [data[i] for i in range(len(data))]

        for pixelIndex in range(len(dataValues) // 4):
            nIndex = ((pixelIndex % width) + ((pixelIndex - (pixelIndex % width)) // width) * width * stretch) * stretch
            for x in range(stretch):
                for y in range(stretch):
                    res[(nIndex + x + (y * width * stretch)) * 4 + 0] = dataValues[(pixelIndex * 4) + 0]
                    res[(nIndex + x + (y * width * stretch)) * 4 + 1] = dataValues[(pixelIndex * 4) + 1]
                    res[(nIndex + x + (y * width * stretch)) * 4 + 2] = dataValues[(pixelIndex * 4) + 2]
                    res[(nIndex + x + (y * width * stretch)) * 4 + 3] = dataValues[(pixelIndex * 4) + 3]

        return width * stretch, height * stretch, res

    def load_image(path: str) -> tuple[int, int, list[int]]:
        width, height, channels, data = dpg.load_image(path)
        return stretch_image(data, width, height, 4)

    def add_texture_to_registry(path):
        width, height, data = load_image(path)
        return dpg.add_static_texture(width=width, height=height, default_value=data)

    with dpg.texture_registry():
        gv.tex_terrain = add_texture_to_registry("src/textures/terrain1.png")
        gv.tex_troop_red = add_texture_to_registry("src/textures/troop1.png")
        gv.tex_troop_blue = add_texture_to_registry("src/textures/troop2.png")
        gv.tex_resource = add_texture_to_registry("src/textures/resource.png")


def gen_terrain():
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            trueCell = Vec((x, 10 - y))
            dpg.add_image(gv.tex_terrain, pos=(trueCell * 64 + Vec((8, 8))).pos, parent="child_window_main_game", border_color=(0, 0, 0, 40))
