# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring, fixme
import json
import pkgutil
from copy import deepcopy
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region
from worlds.AutoWorld import World

from .options import get_option_value

PATH_ITEMS = str(Path("data", "items.json"))


def get_json_data(location: str) -> List[Dict[str, Any]]:
    byte_data = pkgutil.get_data(__name__, location)
    return json.loads(byte_data)


class CelesteItemType(Enum):
    CASSETTE = auto()
    COMPLETION = auto()
    GEMHEART = auto()
    STRAWBERRY = auto()


class CelesteItem(Item):
    game: str = "Celeste"
    item_type: CelesteItemType
    level: int
    side: int

    def __init__(
        self,
        name: str,
        classification: ItemClassification,
        code: Optional[int],
        player: int,
        item_type: CelesteItemType,
        level: int,
        side: int,
    ):
        super().__init__(name, classification, code, player)
        self.item_type = item_type
        self.level = level
        self.side = side

    @staticmethod
    def create_from_pandas(world: World, row: Dict[str, Any]) -> "CelesteItem":
        item_type = CelesteItemType[row["type"].upper()]
        if (
            item_type == CelesteItemType.STRAWBERRY
            and get_option_value(world.multiworld, world.player, "berries_required") == 0
        ):
            classification = ItemClassification.filler
        else:
            classification = ItemClassification.progression

        return CelesteItem(
            f"{row['name']}",
            classification,
            row["id"],
            world.player,
            item_type,
            row["level"],
            row["side"],
        )


class CelesteLocation(Location):
    game: str = "Celeste"
    level: int
    side: int

    # override constructor to automatically mark event locations as such
    def __init__(
        self,
        player: int,
        level: int,
        side: int,
        name: str = "",
        code: Optional[int] = None,
        parent: Optional[Region] = None,
    ):
        super().__init__(player, name, code, parent)
        self.level = level
        self.side = side
        self.event = code is None

    @staticmethod
    def create_from_pandas(world: World, row: Dict[str, Any]) -> "CelesteLocation":
        code = row["id"] if row["level"] < 10 else None
        location = CelesteLocation(world.player, row["level"], row["side"], f"{row['name']}", code)
        if location.level == 9:
            if location.side == 0:
                location.access_rule = lambda state: state.has_group("gemhearts", world.player, 4)
            elif location.side == 1:
                location.access_rule = lambda state: state.has_group("gemhearts", world.player, 15)
            elif location.side == 2:
                location.access_rule = lambda state: state.has_group("gemhearts", world.player, 23)
        if location.level == 10:
            location.progress_type = LocationProgressType.EXCLUDED
            location.access_rule = (
                lambda state: state.has_group(
                    "gemhearts", world.player, get_option_value(world.multiworld, world.player, "hearts_required")
                )
                and state.has_group(
                    "strawberries", world.player, get_option_value(world.multiworld, world.player, "berries_required")
                )
                and state.has_group(
                    "completions", world.player, get_option_value(world.multiworld, world.player, "levels_required")
                )
                and state.has_group(
                    "cassettes", world.player, get_option_value(world.multiworld, world.player, "cassettes_required")
                )
            )
        return location


class CelesteItemFactory:
    _table: List[CelesteItem]
    _map: Dict[str, CelesteItem]
    _loaded: bool = False
    _world: World

    def _load_table(self, world: World, force: bool = False) -> None:
        if force or not self._loaded or self._world != world:
            json_rows = get_json_data(PATH_ITEMS)
            self._table = [CelesteItem.create_from_pandas(world, row) for row in json_rows if row["level"] < 10]
            self._map = {item.name: item for item in self._table}
            self._world = world
            self._loaded = True

    @staticmethod
    def get_name_to_id() -> Dict[str, int]:
        json_rows = get_json_data(PATH_ITEMS)
        return {f"{row['name']}": row["id"] for row in json_rows if row["level"] < 10}

    def create_item(self, item: str) -> CelesteItem:
        self._load_table(self._world)
        return deepcopy(self._map[item])

    def get_table(self, world: World) -> List[CelesteItem]:
        self._load_table(world)
        return self._table


class CelesteLocationFactory:
    _table: List[CelesteLocation]
    _map: Dict[str, CelesteLocation]
    _loaded: bool = False

    def _load_table(self, world: World, force: bool = False) -> None:
        if force or not self._loaded:
            json_rows = get_json_data(PATH_ITEMS)
            self._table = [CelesteLocation.create_from_pandas(world, row) for row in json_rows]
            self._map = {item.name: item for item in self._table}
            self._loaded = True

    @staticmethod
    def get_name_to_id() -> Dict[str, int]:
        json_rows = get_json_data(PATH_ITEMS)
        return {f"{row['name']}": int(row["id"]) for row in json_rows}

    def get_table(self, world: World) -> List[CelesteLocation]:
        self._load_table(world)
        return self._table
