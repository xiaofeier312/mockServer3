import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import MockJson

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context()))

migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    db.create_all(bind=None)

@manager.command
def create_db():
    db.create_all(bind=None)

@manager.command
def init_data():
    m1 = MockJson()
    m1.name='OnlyTest'
    m1.url='/test/test'
    m1.mock_json='{"result":"This is MOCK!"}'
    m1.status = 1
    m1.delay_time = 1
    m1.delay_status = 1
    m1.remark='Zhouzhijun test'
    m1.operator = u'周志军'
    db.session.add(m1)
    db.session.commit()



if __name__ == '__main__':
    manager.run()