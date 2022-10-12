#from knappe.decorators import context, html, json, composed, trigger
#from knappe.response import Response
#from knappe.request import RoutingRequest as Request
#from knappe.routing import Router
#from knappe.ui import SlotExpr, slot, UI, Layout
#from knappe.meta import HTTPMethodEndpointMeta
#from horseman.mapping import RootNode
#from horseman.environ import WSGIEnvironWrapper
from kavalkade.messages import MessageHandler
import discord
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await MessageHandler.onMessage(message)
    

client.run('MTAyNzMwNzA5NjExMjM3Mzg2MA.G1YH41.HN-MMRoDGx3Dr221ghjYdrmJJLlqijoDSy9pdE')