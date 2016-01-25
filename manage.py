from flask.ext.script import Manager, Server
from pastebin import app, db

manager = Manager(app)


@manager.command
def initdb():
    """Creates all database tables."""
    db.create_all()


@manager.command
def dropdb():
    """Drops all database tables."""
    db.drop_all()

manager.add_command('server', Server(host='0.0.0.0', port=9200))


if __name__ == '__main__':
    manager.run()
