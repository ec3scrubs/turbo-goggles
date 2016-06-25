from flask import Flask
import json
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/findroute")
def find_route():
    start = ["567987", "730157", "596195"]
    destinations = [
        "Junction 8",
        "Plaza Singapura",
        "Star Vista",
        "Causeway Point"
    ]
    return json.dumps(start)

if __name__ == "__main__":
    app.run()
