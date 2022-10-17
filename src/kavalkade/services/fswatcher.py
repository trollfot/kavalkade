import inotipy


async def fswatcher(app, *paths) :
    watcher = inotipy.Watcher.create()
    for path in paths :
        watcher.watch(path, inotipy.IN.ALL_EVENTS)
    while True :
        event = await watcher.get()
        if app.websockets:
            await app.websockets.broadcast(f"Got event: {event!r}\n")
