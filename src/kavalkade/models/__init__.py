from kavalkade.app.models import Models

models = Models()


from .character import Character, Item, Action, Note

__all__ = ('models', 'Character', 'Item', 'Action', 'Note')
