import json
from datetime import datetime


def load_clubs():
    with open('clubs.json') as clubs:
        return json.load(clubs)['clubs']


def load_competitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


def get_future_competitions(comps):
    return [comp for comp in comps if datetime.now() < datetime.strptime(comp["date"][2:], '%y-%m-%d %H:%M:%S')]
