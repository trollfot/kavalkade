import typing as t
from pydantic import BaseModel
from kavalkade.models import models


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


@models.register('character')
class Character(BaseModel):
    owner: str
    game: str
    name: str
    portrait: t.Optional[bytes]
    stats: t.Dict[str, t.Union[str, int]] = {}
    inventory: t.List[Item] = []
    actions: t.List[Action] = []
    notes: t.List[Note] = []


__all__ = ('Action', 'Item', 'Note', 'Character')
