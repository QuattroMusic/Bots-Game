from src.configs import RESOURCE_HEALTH, TROOP_DEFAULT_HEALTH, TROOP_DEFAULT_DAMAGE, TROOP_DEFAULT_MOVE_SPEED, MAP_HEIGHT, MAP_WIDTH, BOT_STARTING_RESOURCES


class Vec:
    def __init__(self, pos: list[int, int] | tuple[int, int]):
        self.x: int = pos[0]
        self.y: int = pos[1]
        self.pos = (self.x, self.y)

    def __add__(self, cell2: 'Vec') -> 'Vec':
        """
        Addition of two vectors
        Vec((4, 9)) + Vec((3, 1))  ->  Vec((7, 10))
        """
        return Vec((self.x + cell2.x, self.y + cell2.y))

    def __sub__(self, cell2: 'Vec') -> 'Vec':
        """
        Subtraction of two vectors
        Vec((4, 9)) - Vec((3, 1))  ->  Vec((1, 8))
        """
        return Vec((self.x - cell2.x, self.y - cell2.y))

    def __mul__(self, other: int) -> 'Vec':
        """
        Multiplication with a number or a list
        Vec((2, 2)) * 5  ->  Vec((10, 10))
        """
        return Vec((self.x * other, self.y * other))

    def __truediv__(self, other: int):
        """
        Division with an integer
        Output is an integer
        Vec((10, 5)) / 5  -> Vec((2, 1))
        Vec((8, 5)) / 4   -> Vec((2, 1))
        """
        return Vec((self.x // other, self.y // other))

    def __eq__(self, other: 'Vec'):
        """
        Check if a vector is equal to another
        Vec((3, 5)) == Vec((3, 5))  -> True
        Vec((1, 6)) == Vec((4, 2))  -> False
        """
        return self.x == other.x and self.y == self.y

    def length(self) -> float:
        """
        Get the length of the Vector
        Vec((0, 4)).length()   ->  4.0
        Vec((3, 4)).length()   ->  5.0
        Vec((-2, 6)).length()  ->  6.32...
        """
        return pow(pow(self.x, 2) + pow(self.y, 2), 1 / 2)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
        When printing a Vec
        print(Vec((2, 3)))  -> Vec((2, 3))
        """
        return f"Vec(({self.x}, {self.y}))"


class Resource:
    def __init__(self):
        self.health: int = RESOURCE_HEALTH
        self.position: Vec = Vec((0, 0))


class Bot:
    def __init__(self):
        self.resources: int = BOT_STARTING_RESOURCES
        self.resources_pos: list[Resource] = []
        self.troops: list[Troop] = []
        self.enemies: list[Troop] = []
        self.spawn_pos: Vec = Vec((0, 0))


class Troop:
    def __init__(self):
        self.owner: Bot | None = None
        self.position: Vec = Vec((0, 0))
        self.health: int = TROOP_DEFAULT_HEALTH
        self.move_speed: int = TROOP_DEFAULT_MOVE_SPEED
        self.damage: int = TROOP_DEFAULT_DAMAGE


class Map:
    def __init__(self):
        self.width: int = MAP_WIDTH
        self.height: int = MAP_HEIGHT
        self.map: list[list[None | Troop | Resource]] = [[None for _ in range(self.width)] for _ in range(self.height)]
