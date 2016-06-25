from flask import Flask
import json
import requests
import os

app = Flask(__name__)

settings = ""


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/findroute")
def find_route():
    start_list = ["567987", "730157", "596195", "348271"]
    dest_list = [
        "Junction 8",
        "Plaza Singapura",
        "Nex",
        "JEM",
        "Star Vista",
        "Causeway Point",
        "AMK Hub"
    ]

    start = [Source(x) for x in start_list]
    dest = [Destination(x) for x in dest_list]

    for s in start:
        for d in dest:
            get_time(s, d)

    for d in dest:
        print d.location, d.time

    return "hello"


def get_time(start, dest):
    de_req = "http://www.streetdirectory.com/api/?mode=search&act=all"
    de_req += "&profile=sd_mobile&country=sg&q=" + dest.location
    de_req += "&output=json&start=0&limit=1"

    r = requests.get(de_req)
    resp = json.loads(r.text)
    dest.google_location = resp[1]['a']

    api_key = settings['keys']['google_api']
    req = "https://maps.googleapis.com/maps/api/directions/json?"
    req += "origin=" + start.location
    req += "&destination=" + dest.google_location
    req += "&region=sg&mode=transit&key=" + api_key

    r = requests.get(req)
    resp = json.loads(r.text)
    time = resp['routes'][0]['legs'][0]['duration']['value']
    dest.time += int(time) / 60
    print start.location, dest.location, time / 60


class Destination:
    def __init__(self, loc):
        self.location = loc
        self.google_location = ""
        self.time = 0


class Source:
    def __init__(self, loc):
        self.location = loc


if __name__ == "__main__":
    # Load the configuration
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, 'config.json'), 'r') as config:
        settings = json.load(config)

    app.run()
