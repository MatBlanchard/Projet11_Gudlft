from tests.conftest import clubs, competitions
from utils import get_future_competitions


class TestPointsDisplay:

    clubs = clubs()
    comps = competitions()

    def test_points_display_with_login(self, client, captured_templates):
        # On se connecte à l'application
        club = self.clubs[0]
        email = club['email']
        response = client.post('/show_summary', data={'email': email})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)

        # On affiche la page des points de tout les clubs
        response = client.get('/points_display')
        assert response.status_code == 200
        template, context = captured_templates[1]
        assert template.name == 'points_display.html'
        assert context['clubs'] == self.clubs