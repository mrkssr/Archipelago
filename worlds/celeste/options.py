# pylint: disable=missing-class-docstring, missing-module-docstring, fixme, unused-import

from typing import Dict, Union

from BaseClasses import MultiWorld
from Options import DefaultOnToggle, Range, Toggle


class BerriesRequired(Range):
    """Number of Strawberries required to pass through the Crystal Heart Gate in Chapter 9: Farewell."""

    display_name = "Strawberry Requirement"
    range_start = 0
    range_end = 175
    default = 0


class CassettesRequired(Range):
    """Number of Cassettes required to pass through the Crystal Heart Gate in Chapter 9: Farewell."""

    display_name = "Cassette Requirement"
    range_start = 0
    range_end = 8
    default = 0


class HeartsRequired(Range):
    """Number of Crystal Hearts required to pass through the Crystal Heart Gate in Chapter 9: Farewell."""

    display_name = "Crystal Heart Requirement"
    range_start = 0
    range_end = 24
    default = 15


class LevelsRequired(Range):
    """Number of Level Completions required to pass through the Crystal Heart Gate in Chapter 9: Farewell."""

    display_name = "Level Completion Requirement"
    range_start = 0
    range_end = 24
    default = 0


celeste_options: Dict[str, type] = {
    "berries_required": BerriesRequired,
    "cassettes_required": CassettesRequired,
    "hearts_required": HeartsRequired,
    "levels_required": LevelsRequired,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[bool, int]:
    option = getattr(world, name, None)

    if option is None:
        return 0

    if issubclass(celeste_options[name], Toggle) or issubclass(celeste_options[name], DefaultOnToggle):
        return bool(option[player].value)
    return option[player].value
