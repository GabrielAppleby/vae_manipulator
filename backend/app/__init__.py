import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from app.api.duke_api import DukeAPI, DukeListAPI
from app.dao.database import db

from app.api.model_api import ModelEncodeAPI, ModelDecodeAPI


def create_app() -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    Migrate(app, db)

    api: Api = Api(app, prefix='/api')

    api.add_resource(ModelEncodeAPI, '/model/encode')
    api.add_resource(ModelDecodeAPI, '/model/decode')
    api.add_resource(DukeListAPI, '/duke')
    api.add_resource(DukeAPI, '/duke/<int:uid>')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET')

        return response

    return app


application = create_app()
