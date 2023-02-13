import server
from tests.conftest import clubs, competitions
from utils import get_future_competitions


class TestPurchasePlaces:

    clubs = clubs()
    comps = competitions()

    def test_valid_comp_valid_club_valid_places_should_book(self, client, captured_templates):
        club = self.clubs[0]
        comp_id = 1
        nb_places = 1
        response = client.post('/purchase_places', data={'competition': self.comps[comp_id]['name'],
                                                         'club': club['name'],
                                                         'places': nb_places})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert server.validation_booking in response.data.decode()
        club['points'] = int(club['points']) - nb_places
        assert context['club'] == club
        self.comps[comp_id]['numberOfPlaces'] = int(self.comps[comp_id]['numberOfPlaces']) - nb_places
        assert context['competitions'] == get_future_competitions(self.comps)
        club['points'] = str(int(club['points']) + nb_places)
        self.comps[comp_id]['numberOfPlaces'] = str(int(self.comps[comp_id]['numberOfPlaces']) + nb_places)

    def test_invalid_comp_valid_club_valid_places_should_not_book(self, client, captured_templates):
        club = self.clubs[0]
        nb_places = 1
        response = client.post('/purchase_places', data={'competition': 'invalid_comp',
                                                         'club': club['name'],
                                                         'places': nb_places})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert server.error_default in response.data.decode()
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)

    def test_valid_comp_invalid_club_valid_places_should_return_index_page(self, client, captured_templates):
        comp = self.comps[1]
        nb_places = 1
        response = client.post('/purchase_places', follow_redirects=True, data={'competition': comp['name'],
                                                                                'club': 'invalid_club',
                                                                                'places': nb_places})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "index.html"
        assert server.error_default in response.data.decode()

    def test_valid_comp_valid_club_invalid_places_type_should_not_book(self, client, captured_templates):
        comp = self.comps[1]
        club = self.clubs[0]
        response = client.post('/purchase_places', data={'competition': comp['name'],
                                                         'club': club['name'],
                                                         'places': 'invalid_places'})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert server.error_default in response.data.decode()
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)

    def test_valid_comp_valid_club_invalid_places_should_not_book(self, client, captured_templates):
        comp = self.comps[1]
        club = self.clubs[0]
        nb_places = 15
        response = client.post('/purchase_places', data={'competition': comp['name'],
                                                         'club': club['name'],
                                                         'places': nb_places})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert server.error_default in response.data.decode()
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)
