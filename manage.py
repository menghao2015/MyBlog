#!/usr/bin/env python
import os
from myapp import create_app, db
from myapp.models import User, Role, Post, Student, Class, Follow, Comment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

apl = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(apl)
migrate = Migrate(apl, db)


def make_shell_context():
    return dict(apl=apl, db=db, User=User, Role=Role, Post=Post, Student=Student, Class=Class, Follow=Follow, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
	from flask.ext.migrate import upgrade
	from myapp.models import Role, User

	db.create_all()
	Role.insert_roles()


if __name__ == '__main__':
    manager.run()
