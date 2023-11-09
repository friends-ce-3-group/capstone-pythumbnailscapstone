# app.py
from flask import Flask, request, json

app = Flask(__name__)

import healthcheck

import thumbnail

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')