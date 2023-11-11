# pylint: disable=missing-class-docstring, missing-module-docstring, fixme
from copy import deepcopy

from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import MultiWorld, WebWorld, World

from .items import (
    CelesteItem,
    CelesteItemFactory,
    CelesteItemType,
    CelesteLocationFactory,
)
from .options import CelesteOptions
from .regions import CelesteRegionFactory


class CelesteWebWorld(WebWorld):
    theme = "ice"
    tutorials = [
        Tutorial(
            "Multiworld Setup Tutorial",
            "A guide to setting up the Celeste randomiser connected to an Archipelago MultiWorld.",
            "English",
            "celeste_en.md",
            "celeste/en",
            ["doshyw"],
        )
    ]


class CelesteWorld(World):
    """
    Help Madeline survive her inner demons on her journey to the top of Celeste Mountain, in this super-tight,
    hand-crafted platformer from the creators of multiplayer classic TowerFall.
    """

    game = "Celeste"
    options_dataclass = CelesteOptions
    options: CelesteOptions
    topology_present = True
    web = CelesteWebWorld()

    item_factory: CelesteItemFactory
    location_factory: CelesteLocationFactory
    region_factory: CelesteRegionFactory

    item_name_to_id = CelesteItemFactory.get_name_to_id()
    location_name_to_id = CelesteLocationFactory.get_name_to_id()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.item_factory = CelesteItemFactory()
        self.location_factory = CelesteLocationFactory()
        self.region_factory = CelesteRegionFactory()

    def create_item(self, name: str) -> Item:
        return self.item_factory.create_item(name)

    def create_regions(self):
        self.region_factory.activate(self)

    def create_items(self):
        item_table = self.item_factory.get_table(self)

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
