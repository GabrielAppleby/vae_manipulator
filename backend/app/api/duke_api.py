import numpy as np
from typing import Dict

from flask_restful import fields, Resource, marshal_with

from app.dao.duke_dao import DukeDB


class BytesField(fields.Raw):
    def format(self, value):
        return np.frombuffer(value).astype(float).tolist()


duke_fields: Dict = {
    "uid": fields.Integer,
    "label": fields.String,
    "url": fields.String,
    "x": fields.Float,
    "y": fields.Float,
    # "embedding": BytesField
}


class DukeListAPI(Resource):
    @marshal_with(duke_fields)
    def get(self):
        return DukeDB.query.all()


class DukeAPI(Resource):
    @marshal_with(duke_fields)
    def get(self, uid):
        return DukeDB.query.get_or_404(uid)
