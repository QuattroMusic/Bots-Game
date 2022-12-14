from src.battle.objects import Bot, Troop, Vec, Map, Resource

# various
bots: list[tuple[str, callable, Bot | None]] = [("", None, None), ("", None, None)]
world_map: Map = Map()
is_game_running = False
waiting_to_stop_game = False
sleep_time = 0.2
turn = 0

# dpg stuff
viewport_width = 1300
viewport_height = 777
tex_terrain, tex_troop_blue, tex_troop_red, tex_resource = -1, -1, -1, -1
troop_id, resource_id = -1, -1

# commands
commands_move: list[tuple[Troop, Vec, int]] = []
commands_action: list[tuple[Troop, Vec]] = []
commands_powerup: list[tuple[Troop, str]] = []
commands_create: list[Bot] = []

# mappers
map_troop_to_id: dict[Troop, str] = {}
map_resource_to_id: dict[Resource, str] = {}

# final statistics
stat_bots_resources_trend: dict[Bot, list[int]] = {}
stat_bots_eliminated_troops: dict[Bot, int] = {}
stat_bots_eliminated_resources: dict[Bot, int] = {}
stat_bots_created_troops: dict[Bot, int] = {}
stat_bots_used_resources: dict[Bot, dict[str, int]] = {}
stat_bots_troops_kills: dict[Bot, dict[Troop, int]] = {}
stat_bots_troops_resources: dict[Bot, dict[Troop, int]] = {}
