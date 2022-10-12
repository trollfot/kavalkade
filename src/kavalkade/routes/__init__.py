from knappe.decorators import html, json, composed, trigger
from knappe.routing import Router

from kavalkade.controllers.index import Index

router = Router()

router.register('/')(Index)