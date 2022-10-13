import typing as t
from pydantic import BaseModel


class Action:
    """Character action.
    """
    name: str


class Item:
    """Inventory item.
    """
    name: str


class Note:
    """Gamemaster note
    """
    name: str
    content: str


class Character(BaseModel):
    owner: str
    game: str
    name: str
    portrait: t.Optional[bytes]
    stats: t.Dict[str, t.Union[str, int]] = {}
    inventory: t.List[Item] = []
    actions: t.List[Action] = []
    notes: t.List[Note] = []
