from utils import load_competitions, load_clubs
from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    clubs = load_clubs()
    comps = load_competitions()

    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post('/show_summary', {'email': self.clubs[0]['email']})

    @task
    def purchase_points(self):
        self.client.post('/purchase_places', {'club': self.clubs[0]['name'],
                                              'competition': self.comps[0]['name'],
                                              'places': 1})
