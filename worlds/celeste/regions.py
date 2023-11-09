from typing import Callable, Optional

from BaseClasses import CollectionState, Region
from worlds.AutoWorld import World

from .items import CelesteLocationFactory

SIDE_MAP = {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 1}
SIDE_LETTERS = ["A", "B", "C"]


class CelesteRegionFactory:
    _world: World

    @classmethod
    def _add_region(cls, region: Region) -> Region:
        cls._world.multiworld.regions.append(region)
        return region

    @classmethod
    def _construct_rule(cls, level: int, side: int) -> Optional[Callable[[CollectionState], bool]]:
        if side == 0:
            if level == 1:
                return None
            return lambda state: state.has_any(
                {f"ITEM_COMPLETION_{level - 1}A", f"ITEM_COMPLETION_{level - 1}B", f"ITEM_COMPLETION_{level - 1}C"},
                cls._world.player,
            )
        elif side == 1:
            return lambda state: state.has(f"ITEM_CASSETTE_{level}A", cls._world.player)
        elif side == 2:
            return lambda state: state.has_all(
                {f"ITEM_GEMHEART_{level}A", f"ITEM_GEMHEART_{level}B"}, cls._world.player
            )
        else:
            return None

    @classmethod
    def activate(cls, world: World) -> None:
        cls._world = world

        menu_region = cls._add_region(Region("Menu", cls._world.player, cls._world.multiworld))
        map_region = cls._add_region(Region("Map", cls._world.player, cls._world.multiworld))
        menu_region.connect(map_region)

        location_table = CelesteLocationFactory.get_table(cls._world)

        for level, count in SIDE_MAP.items():
            for side in range(count):
                level_name = f"Level {level} {SIDE_LETTERS[side]}-Side"
                level_region = cls._add_region(Region(level_name, cls._world.player, cls._world.multiworld))
                map_region.connect(level_region, level_name, cls._construct_rule(level, side))
                native_locations = [
                    location for location in location_table if location.level == level and location.side == side
                ]
                for location in native_locations:
                    level_region.locations.append(location)
                    location.parent_region = level_region
