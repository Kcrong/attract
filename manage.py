# -*-coding: utf-8 -*-

from app import manager, create_app

app = create_app()


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
