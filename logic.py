from abc import ABC, abstractmethod

import utils._display as _display
import utils._general as _general

import random
import math

from typing import Optional

random.seed()

Scene_current = "game"

camera_range_x = 65
camera_range_y = 41
camera_pos_x, camera_pos_y = 0, 0
inv_i, hotbar_i = 0, 0

class Scene(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def display(self):
        pass

terrain_type = dict[
    str: int
]
structure_type = dict[
    str: tuple[
        tuple[str],
        int
    ]
]
biome_type = dict[
    "terrain": terrain_type,
    "structure": structure_type
]

biomes: dict[str: biome_type] = {
    "grassland": {
        "terrain": {
            f"🟩": 0.5,
            f"🟨": 0.4,
            f"🟦": 0,
        },
        "structure": {
            "🌳": (("🟩"), 0.01),
            "🌴": (("🟨"), 0.01),
            "🎄": (("🟩", "🟨"), 0.001)
        }
    },
    "desert": {
        "terrain": {
            "🟦": 0.9,
            "🟨": 0,
        },
        "structure": {
            "🌵": (("🟩"), 0.02),
            "🌴": (("🟨"), 0.01)
        }
    }
}

class Biome():
    def __init__(self,
        biome: str = "grassland",
        x: int = 0,
        y: int = 0,
        radius: int = 50,
    ):
        self.biome: biome_type = biomes[biome]
        self.x = x
        self.y = y
        self.radius = radius

class Game(Scene):
    def __init__(self,
        name: str,
        x: int = 500,
        y: int = 500,
        iterations: int = 4,
        baseBiome: biome_type = biomes["grassland"],
        spawnTiles: tuple = ("🟩", "🟨")
    ):
        assert isinstance(name, str)
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(iterations, int)
        assert isinstance(baseBiome, dict)
        assert isinstance(spawnTiles, tuple)
        
        self.name = name or ""
        self.x = x
        self.y = y
        self.iterations = iterations
        self._baseBiome = baseBiome
        # self._terrain = _general.sort_dict(terrain, lambda i: i[1], True)
        # self._structure = _general.sort_dict(structure, lambda i: i[1][1])
        self.spawnTiles = spawnTiles
        self.map = {}
        self.biome = {}
        self.entities = []

    def display(self, camera_rx: int = camera_range_x, camera_ry: int = camera_range_y) -> str:
        assert isinstance(camera_rx, int)
        assert isinstance(camera_ry, int)

        x = self.x
        y = self.y
        map = self.map
        entities = self.entities

        result = ""

        for cam_iy in range(camera_ry):
            for cam_ix in range(camera_rx):
                xx = camera_pos_x + (cam_ix % camera_rx) - math.floor(camera_rx / 2)
                yy = camera_pos_y - cam_iy + math.floor(camera_ry / 2)
                
                weight = None
                for entity in entities:
                    if xx == entity.x and yy == entity.y:
                        weight = entity.graphic
                        break

                if not weight:
                    if xx >= 0 and xx <= (x - 1) and yy >= 0 and yy <= (y - 1):
                        weight = map[yy][xx]
                    else:
                        weight = "⬛"
                
                result += weight
                
            result += "\n"

        return result
    
    def getPosition(self, x: int, y: int) -> Optional[str]:
        assert isinstance(x, int)
        assert isinstance(y, int)
        
        if y in self.map and x in self.map[y]:
            return self.map[y][x]
        else:
            return None


    def findSpawn(self) -> Optional[tuple[int, int, str]]:
        x = self.x
        y = self.y

        while True:
            s_x = random.randint(0, x - 1)
            s_y = random.randint(0, y - 1)
            tile = self.getPosition(s_x, s_y)
            
            if tile in self.spawnTiles:
                break

        return s_x, s_y, tile

    def generate_map(self, iterations: int = None, batch: dict = {}) -> dict:
        iterations = iterations or self.iterations
        assert isinstance(iterations, int)
        assert isinstance(batch, dict)

        x = self.x
        y = self.y
        _terrain = self._baseBiome["terrain"]
        _structure = self._baseBiome["structure"]

        tiles_loaded = 0
        tiles_to_load = self.x * self.y * iterations

        lowest, highest = 1, 0

        
        for int_i in range(iterations + 1):
            result = {}

            for y_i in range(x):
                result[y_i] = {}
                for x_i in range(y):
                    if int_i < iterations:
                        weight = 0

                        if len(batch) == 0:
                            weight = random.uniform(0, 1)
                        else:
                            new_value = 0
                            neighbors = 0

                            for neighbor_i in range(9):
                                xx = x_i + ((neighbor_i % 3) - 1)
                                yy = y_i + (math.floor(neighbor_i / 3) - 1)
                                
                                if (xx >= 0 and xx <= (x - 1) and yy >= 0 and yy <= (y - 1)):
                                    new_value += batch[yy][xx]
                                    neighbors += 1
                                
                            weight = new_value / neighbors

                        lowest, highest = min(lowest, weight), max(highest, weight)
                        result[y_i][x_i] = weight

                        tiles_loaded += 1
                        if (tiles_loaded % math.floor(tiles_to_load / 100) == 0):
                            _display.loading_bar(f"loading {self.name}...", tiles_loaded, tiles_to_load)

                    else:
                        weight = (batch[y_i][x_i] - lowest) / (highest - lowest)

                        for terrain in _terrain:
                            if weight >= _terrain[terrain]: # threshold
                                weight = terrain # base

                                for structure in _structure:
                                    structure_info = _structure[structure]
                                    if weight in structure_info[0] and random.uniform(0, 1) <= structure_info[1]: # threshold
                                        weight = structure # overriden structure
                                        break
                                break

                        result[y_i][x_i] = weight
                    
            batch = result
        self.map = result
        
        return result
        
class Entity(ABC):
    def __init__(self,
        graphic: str,
        x: int = 0,
        y: int = 0,
        game: Game = None
    ):
        assert isinstance(graphic, str)
        assert isinstance(x, int)
        assert isinstance(y, int)

        self.x = x
        self.y = y
        self.graphic = graphic
        self.game = None
        self.setGame(game)
    
    def _removeGame(self):
        game = self.game
        if game:
            entities = game.entities
            entities.pop(entities.index(self))
            self.game = None

    def setGame(self, game: Game):
        assert isinstance(game, Game)

        self._removeGame()
        game.entities.append(self)
        self.game = game

    def destroy(self):
        self._removeGame()
        del self




