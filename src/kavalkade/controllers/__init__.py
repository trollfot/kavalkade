from knappe.routing import Router

router = Router()


from .profile import Profile
from .index import Index
from .models import model_schema

__all__ = ('Profile', 'Index', 'model_schema')
