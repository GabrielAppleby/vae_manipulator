from io import BytesIO
from typing import List
from urllib.parse import urlparse

import requests
from flask import request, send_file, Response
from flask_restful import Resource

from app.core.modeling import predict, decode


class ModelEncodeAPI(Resource):
    def post(self) -> Response:
        url1 = request.args.get('url1')
        url2 = request.args.get('url2')
        url3 = request.args.get('url3')
        if url2:
            pr1 = urlparse(url1)
            file1 = requests.get('http://images/images/{}'.format(pr1.path)).content
            pr2 = urlparse(url2)
            file2 = requests.get('http://images/images/{}'.format(pr2.path)).content
            pr3 = urlparse(url3)
            file3 = requests.get('http://images/images/{}'.format(pr3.path)).content
            test = predict(file1, file2, file3)
            file_object = BytesIO()
            test.save(file_object, 'PNG')
            file_object.seek(0)

            return send_file(file_object, mimetype='image/PNG')
        return None


class ModelDecodeAPI(Resource):
    def post(self) -> List[float]:
        json = request.get_json()
        embedding = json['embedding']
        temperature = json['temperature']
        test = decode(embedding, temperature)
        file_object = BytesIO()
        test.save(file_object, 'PNG')
        file_object.seek(0)

        return send_file(file_object, mimetype='image/PNG')
