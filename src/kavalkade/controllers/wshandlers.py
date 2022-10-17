from . import websockets


@websockets.register('/chat')
async def asynchat(app, ws, **params):
    while True:
        m = await ws.recv()
        if m is None:
            break
        await app.websockets.broadcast(m)
