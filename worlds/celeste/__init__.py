# pylint: disable=missing-class-docstring, missing-module-docstring, fixme
from copy import deepcopy

from BaseClasses import Item, ItemClassification, MultiWorld
from Utils import visualize_regions
from worlds.AutoWorld import World

from .items import (
    CelesteItem,
    CelesteItemFactory,
    CelesteItemType,
    CelesteLocationFactory,
)
from .options import CelesteOptions
from .regions import CelesteRegionFactory


class CelesteWorld(World):
    game = "Celeste"
    options_dataclass = CelesteOptions
    options: CelesteOptions
    topology_present = True

    item_name_to_id = CelesteItemFactory.get_name_to_id()
    location_name_to_id = CelesteLocationFactory.get_name_to_id()

    def create_item(self, name: str) -> Item:
        return CelesteItemFactory.create_item(name)

    def create_regions(self):
        CelesteRegionFactory.activate(self)

    def create_items(self):
        item_table = CelesteItemFactory.get_table(self)

        for item in item_table:
            self.multiworld.itempool.append(deepcopy(item))

        self.item_name_groups = {
            "cassettes": [item.name for item in item_table if item.item_type == CelesteItemType.CASSETTE],
            "completions": [item.name for item in item_table if item.item_type == CelesteItemType.COMPLETION],
            "gemhearts": [item.name for item in item_table if item.item_type == CelesteItemType.GEMHEART],
            "strawberries": [item.name for item in item_table if item.item_type == CelesteItemType.STRAWBERRY],
        }

    def generate_basic(self) -> None:
        self.multiworld.get_location("Level 10 A-Side Complete", self.player).place_locked_item(
            CelesteItem("Victory", ItemClassification.progression, None, self.player, CelesteItemType.COMPLETION, 10, 0)
        )
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        return self.options.as_dict("berries_required", "cassettes_required", "hearts_required", "levels_required")
