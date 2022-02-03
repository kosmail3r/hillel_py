import logging
import random

import aiohttp
from aiohttp import web
import aiohttp_jinja2

log = logging.getLogger(__name__)


async def index(request):
    # Django: render(request, 'index.html', {})
    return aiohttp_jinja2.render_template('index.html', request, {})


async def chat(request):
    current_ws = web.WebSocketResponse()

    # пытаемся открыть web socket
    await current_ws.prepare(request)

    name = random.choice(['Alex', 'Marie', 'John', 'Anna'])

    await current_ws.send_json({'action': 'connected',
                                'name': name})

    # Notify all: new user joined
    for ws in request.app['users'].values():
        await ws.send_json({'action': 'join',
                            'name': name})

    request.app['users'][name] = current_ws

    # while True:
    #    data = sock.recv()

    # while True:
    #    msg = await ws.receive() # recv

    async for msg in current_ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            for ws in request.app['users'].values():
                await ws.send_json({'action': 'message',
                                    'message': msg.data})
        else:
            break

    # Notify all: new user disconnected
    for ws in request.app['users'].values():
        await ws.send_json({'action': 'disconnected',
                            'name': name})

    del request.app['users'][name]

    return current_ws
