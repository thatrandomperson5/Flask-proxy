from flask import Flask, request, abort
from base64 import b64decode
import json, requests
from utils import url_re, browser_agents
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Luanch test"

def makePageRender(url, browser):
    if browser is None:
        browser = "inherit"
    if not browser == "inherit":
        if not browser in browser_agents:
            return "Invalid browser"
    if browser == "inherit":
        br = request.headers.get('User-Agent')
    else:
        br = browser_agents.get(browser)
    rqheaders = {"User-Agent": br}
    rq = requests.get(url, headers=rqheaders)
    if not rq.status_code in range(200, 299):
        return "Request Error"
    soup = BeautifulSoup(rq.content, 'html.parser')
    HttpProxyConnector = '''
    console.log("Setting up proxy")
    window.addEventListener('load', () => {
        if (!('serviceWorker' in navigator)) {
        // service workers not supported
        return
    }

    navigator.serviceWorker.register('/static/HttpHandler.js').then(
            () => {
             // 
            },
            err => {
            console.error('Service Worker registration failed!', err)
        }
        )
    })
    '''
    script = soup.new_tag("script")
    script.string = HttpProxyConnector
    soup.head.append(script)
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
    output = makePageRender(url, args.get("browser"))
    return output
