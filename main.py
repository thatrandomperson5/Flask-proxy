from flask import Flask, request, abort
from base64 import b64decode
import json, requests
from utils import url_re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Luanch test"

def makePageRender(url):
    rq = requests.get(url)
    if not rq.status_code in range(200, 299):
        abort(403)
    soup = BeautifulSoup(rq.content, 'html.parser')
    HttpProxyConnector = """
    console.log('test')
    """
    script = soup.new_tag("script")
    script.string = HttpProxyConnector
    soup.head.insert(script)
    return soup.prettify()

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
    output = makePageRender(url)
    return output
