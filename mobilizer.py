import os
from flask import *
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from Models.models import db

engine = create_engine('sqlite:///mobilizer.db')
metadata = MetaData()

app = Flask(__name__, static_folder='mobilizer-app/build')
CORS(app)
app.register_blueprint(Blueprint('static_bp', __name__, static_folder='assets', static_url_path=''), url_prefix='/assets')

api = Api(app)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development_key',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'mobilizer.db')
))
app.config.from_object(__name__)
app.config.from_envvar('CHAT_CONFIG', silent=True)
db.init_app(app)


#Resource API AUTH
from API import resources

api.add_resource(resources.SeeMobilizees, '/mobilizer/seeMobilizees')
api.add_resource(resources.MakeNote, '/mobilizer/addnote')
api.add_resource(resources.RequestRemoval, '/mobilizer/removal')
api.add_resource(resources.TestContact, '/test')
api.add_resource(resources.UpdateContact, '/mobilizer/update')
api.add_resource(resources.AssignMobilizees, '/coordinator/assign')
api.add_resource(resources.RegisterMobilizer, '/coordinator/register_mobilizer')
api.add_resource(resources.ChangePasswordMobilizer, '/mobilizer/change_password')
api.add_resource(resources.RegisterMobilizee, '/coordinator/register_mobilizee')
api.add_resource(resources.MassRegistration, '/coordinator/mass_register')
api.add_resource(resources.RemoveMobilizer, '/coordinator/remove_mobilizer')
api.add_resource(resources.RemoveMobilizee, '/coordinator/remove_mobilizee')
api.add_resource(resources.DeleteMobilizee, '/coordinator/delete_mobilizee')
api.add_resource(resources.UnattachedMobilizees, '/coordinator/unattached_mobilizees')
api.add_resource(resources.SeeMobilizers, '/coordinator/see_mobilizers')
api.add_resource(resources.Login, '/login')

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()

    con = engine.connect()
    con.execute("""INSERT INTO coordinator
                    VALUES (
                        1,
                        'username',
                        '$pbkdf2-sha256$29000$X6sVIiREaG0NQSjl3BtjzA$WhUNyD7BYxY.fHbbpppVxrj.NRbYm1w1F7LHXb6eavQ'
                    );""")

    con.execute("""INSERT INTO mobilizer
                        VALUES (
                            1,
                            'Testing Lastname',
                            'username',
                            '$pbkdf2-sha256$29000$X6sVIiREaG0NQSjl3BtjzA$WhUNyD7BYxY.fHbbpppVxrj.NRbYm1w1F7LHXb6eavQ',
                            'testing@gmail.com',
                            '5103044525',
                            1
                        );""")
    con.execute("""INSERT INTO mobilizer
                            VALUES (
                                2,
                                'Firstname Lastname2',
                                'username2',
                                 '$pbkdf2-sha256$29000$X6sVIiREaG0NQSjl3BtjzA$WhUNyD7BYxY.fHbbpppVxrj.NRbYm1w1F7LHXb6eavQ',
                                'testing2@gmail.com',
                                '5103044524',
                                1
                            );""")



if __name__ == '__main__':
    app.run()