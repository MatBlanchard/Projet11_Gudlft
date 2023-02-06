from datetime import datetime


def get_future_competitions(comps):
    return [comp for comp in comps if datetime.now() < datetime.strptime(comp["date"][2:], '%y-%m-%d %H:%M:%S')]
