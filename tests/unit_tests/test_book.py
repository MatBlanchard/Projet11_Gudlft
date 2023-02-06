import server
from tests.unit_tests.conftest import clubs, competitions
from utils import get_future_competitions


class TestBook:

    clubs = clubs()
    comps = competitions()

    def test_valid_comp_and_valid_club_should_return_booking_page(self, client, captured_templates):
        club = self.clubs[0]
        comp = self.comps[1]
        response = client.get(f"/book/{comp['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "booking.html"
        assert context['club'] == club
        assert context['competition'] == comp

    def test_club_with_more_than_12_points_should_return_12_max_places(self, client, captured_templates):
        club = self.clubs[0]
        assert int(club['points']) > 12
        comp = self.comps[1]
        response = client.get(f"/book/{comp['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "booking.html"
        assert context['club'] == club
        assert context['competition'] == comp
        assert context['max_places'] == 12

    def test_club_with_less_than_12_points_should_return_club_points_as_max_places(self, client, captured_templates):
        club = self.clubs[1]
        assert int(club['points']) < 12
        comp = self.comps[1]
        response = client.get(f"/book/{comp['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "booking.html"
        assert context['club'] == club
        assert context['competition'] == comp
        assert context['max_places'] == int(club['points'])

    def test_club_with_exactly_12_points_should_return_club_points_as_max_places(self, client, captured_templates):
        club = self.clubs[2]
        assert int(club['points']) == 12
        comp = self.comps[1]
        response = client.get(f"/book/{comp['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "booking.html"
        assert context['club'] == club
        assert context['competition'] == comp
        assert context['max_places'] == int(club['points'])

    def test_invalid_comp_and_valid_club_should_return_welcome_page(self, client, captured_templates):
        club = self.clubs[0]
        response = client.get(f"/book/invalid_comp/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)
        assert server.error_default in response.data.decode()

    def test_valid_comp_and_invalid_club_should_return_welcome_page(self, client, captured_templates):
        comp = self.comps[1]
        response = client.get(f"/book/{comp['name']}/invalid_club")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert context['competitions'] == get_future_competitions(self.comps)
        assert server.error_default in response.data.decode()

    def test_invalid_comp_and_invalid_club_should_return_welcome_page(self, client, captured_templates):
        response = client.get(f"/book/invalid_comp/invalid_club")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert context['competitions'] == get_future_competitions(self.comps)
        assert server.error_default in response.data.decode()

    def test_past_comp_and_valid_club_should_return_welcome_page(self, client, captured_templates):
        club = self.clubs[0]
        comp = self.comps[0]
        response = client.get(f"/book/{comp['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)
        assert server.error_default in response.data.decode()