import server
from tests.unit_tests.conftest import clubs, competitions
from utils import get_future_competitions
class TestShowSummary:

    clubs = clubs()
    comps = competitions()

    def test_valid_email_should_return_welcome_page(self, client, captured_templates):
        club = self.clubs[0]
        email = club['email']
        response = client.post('/show_summary', data={'email': email})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)

    def test_invalid_email_should_return_index_page(self, client, captured_templates):
        email = 'invalid@email.com'
        response = client.post('/show_summary', data={'email': email}, follow_redirects=True)
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'index.html'
        assert server.error_email in response.data.decode()
