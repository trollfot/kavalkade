import asyncio
from datetime import datetime


async def clock(app, timeout):
    while True:
        if app.websockets:  # only if there's someone to listen.
            now = datetime.now()
            await app.websockets.broadcast(
                f"It's {now.strftime('%H:%M:%S')}")
        await asyncio.sleep(timeout)


async def services_status(app, timeout):
    while True:
        if app.services and app.websockets:
            for service in app.services:
                await app.websockets.broadcast(
                    f"{service.name}: {service.status}")
        await asyncio.sleep(timeout)
