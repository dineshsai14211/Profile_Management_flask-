import json
from flask import Flask, jsonify, request, redirect, url_for
import requests

app = Flask('__name__')


def status_check(res_json):
    if res_json["status"] == "success":
        return True
    if res_json["status"] == "failed":
        return False


@app.route('/check', methods=["GET", "PUT", "POST", "PATCH", "DELETE"])
def check():
    try:
        data = request.args
        url = data["url"]
        method = request.method
        if method == "GET":
            response = requests.get(url)
            response_json = response.json()
            return jsonify(response_json), 200

        elif method == "POST":
            response = requests.post(url)
            response_json = response.json()
            if status_check(response_json):
                payload = request.get_json()
                return jsonify(payload), 200
            else:
                return jsonify(response_json), response.status_code

        elif method == "PUT":
            response = requests.put(url)
            response_json = response.json()
            if status_check(response_json):
                payload = request.get_json()
                return jsonify(payload), 200
            else:
                return jsonify(response_json), response.status_code

        elif method == "PATCH":
            response = requests.patch(url)
            response_json = response.json()
            if status_check(response_json):
                payload = request.get_json()
                return jsonify(payload), 200
            else:
                return jsonify(response_json), response.status_code

        elif method == "DELETE":
            response = requests.delete(url)
            response_json = response.json()
            if status_check(response_json):
                payload = request.get_json()
                return jsonify(payload), 200
            else:
                return jsonify(response_json), response.status_code

        else:
            raise Exception(f'Incorrect Http request,check it once')
    except Exception as err:
        return jsonify(message=str(err), status="failed"), 400


app.run(debug=True, port=6000)
