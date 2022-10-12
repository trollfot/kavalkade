from knappe.routing import Router

from kavalkade.controllers.index import Index
from kavalkade.controllers.profile import Profile

router = Router()

router.register('/')(Index)
router.register('/profile')(Profile)
