from flask import Flask

from garageberry import GarageDoor

gd = GarageDoor(17, 27, 22)

app = Flask(__name__)


@app.route("/")
def root():
    return f'<p>Garage Door: {gd.door_status}</p>'
