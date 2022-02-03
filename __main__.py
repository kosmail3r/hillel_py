import logging

from aiohttp import web
import jinja2
import aiohttp_jinja2

from chat_demo import views


async def init_app():
    app = web.Application()
    app['users'] = {}
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('chat_demo', 'templates'))
    app.router.add_get('/', views.index)
    app.router.add_get('/chat', views.chat)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
