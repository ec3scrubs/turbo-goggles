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
        "jem 50 jurong gateway",
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
        print d.location, d.google_location, d.time

    return "hello"


def get_time(start, dest):
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
        self.time = 0
        self.google_location = ""
        self.get_location()

    def get_location(self):
        api_key = settings['keys']['google_api']

        req = "https://maps.googleapis.com/maps/api/place/autocomplete/json?"
        req += "key=" + api_key + "&input=" + self.location

        r = requests.get(req)
        resp = json.loads(r.text)
        self.google_location = resp['predictions'][0]['description']


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
