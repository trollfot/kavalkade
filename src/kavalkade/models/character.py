from enum import Enum
import typing as t
from pydantic import BaseModel, Field
from kavalkade.models import models


class PossibleStat(str, Enum):
    str = 'strength'
    dex = 'dexterity'


@models.register('stat')
class Stat(BaseModel):
    """Character stat."""
    name: PossibleStat
    value: int = Field(..., gt=0, le=20)


@models.register('action')
class Action(BaseModel):
    """Character action."""
    name: str


@models.register('inventory_item')
class Item(BaseModel):
    """Inventory item."""
    name: str


@models.register('gm_note')
class Note(BaseModel):
    """Gamemaster note"""
    name: str
    content: str


@models.register('character', addable=True)
class Character(BaseModel):

    class Config:
        underscore_attrs_are_private = True

    owner: str
    game: str
    name: str
    portrait: t.Optional[bytes]
    stats: t.List[Stat] = []
    inventory: t.List[Item] = []
    actions: t.List[Action] = []
    notes: t.List[Note] = []
    _doc_id: t.Optional[int] = Field(alias="doc_id", default=None)


__all__ = ('Action', 'Item', 'Note', 'Character')
