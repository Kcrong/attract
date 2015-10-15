# -*-coding: utf-8 -*-

from app import create_app, manager

app = create_app()


@manager.command
def run():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    manager.run()
