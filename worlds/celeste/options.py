# pylint: disable=missing-class-docstring, missing-module-docstring, fixme, unused-import

from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, Toggle


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


# By convention, we call the options dataclass `<world>Options`.
# It has to be derived from 'PerGameCommonOptions'.
@dataclass
class CelesteOptions(PerGameCommonOptions):
    berries_required: BerriesRequired
    cassettes_required: CassettesRequired
    hearts_required: HeartsRequired
    levels_required: LevelsRequired
