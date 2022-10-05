from flask import Flask, request
from base64 import b64decode
import json
from utils import url_re

app = Flask(__name__)

@app.route("/")
def home():
    return "Luanch test"
@app.route("/tools/pagerender")
def pageRender():
    args = request.args
    if "b64" in args:
        args = json.loads(b64decode(args.get("b64")))
    if not "url" in args:
        return "Invalid url"
    url = args.get("url")
    if not url_re.match(url):
        return "Invalid url"
    return "Ok"
