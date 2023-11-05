from __future__ import annotations
from abc import ABC

import msgspec

import typing as T

if T.TYPE_CHECKING:
    from simulators.cards import Card

CardId = str


class AbstractCardListStruct(msgspec.Struct, array_like=True):
    cards: list[CardId] = msgspec.field(default_factory=list)


class CrafterHandStruct(AbstractCardListStruct):
    pass


class LaneStruct(AbstractCardListStruct):
    slots_modifier: list[int] = msgspec.field(default_factory=list)


class LaneStateStruct(LaneStruct):
    pass


class ReserveLaneStruct(LaneStruct):
    pass


class CrafterState(msgspec.Struct):
    endurance: int
    skill: int
    energy: int = 0


class AtelierStruct(msgspec.Struct):
    lane: LaneStateStruct
    reserve: ReserveLaneStruct
    damage_resistance: int = 0
    complexity: int = 0


class VisibleGameStateStruct(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """
    Game State that is visible to the player (or an I.A. acting as the player)
    """
    turn: int
    crafter: CrafterState
    turn_modifier: int = 0
    crafter_hand: CrafterHandStruct
    atelier: AtelierStruct

    @property
    def lane(self):
        return self.atelier.lane

    @property
    def reserve(self):
        return self.atelier.reserve


