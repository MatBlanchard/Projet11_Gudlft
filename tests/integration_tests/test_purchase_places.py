import server
from tests.conftest import clubs, competitions
from utils import get_future_competitions


class TestPurchasePlaces:

    clubs = clubs()
    comps = competitions()

    def test_purchase_places_with_login_then_logout(self, client, captured_templates):
        # On se connecte à l'application
        club = self.clubs[0]
        email = club['email']
        comp_id = 1
        nb_places = 1
        response = client.post('/show_summary', data={'email': email})
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert context['competitions'] == get_future_competitions(self.comps)

        # On affiche la page de booking d'une compétition
        response = client.get(f"/book/{self.comps[comp_id]['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[1]
        assert template.name == "booking.html"
        assert context['club'] == club
        assert context['competition'] == self.comps[comp_id]
        assert context['max_places'] == 12

        # On réserve des places pour cette compétition
        response = client.post('/purchase_places', data={'competition': self.comps[comp_id]['name'],
                                                         'club': club['name'],
                                                         'places': nb_places})
        assert response.status_code == 200
        template, context = captured_templates[2]
        assert template.name == "welcome.html"
        assert server.validation_booking in response.data.decode()
        club['points'] = int(club['points']) - nb_places
        assert context['club'] == club
        self.comps[comp_id]['numberOfPlaces'] = int(self.comps[comp_id]['numberOfPlaces']) - nb_places
        assert context['competitions'] == get_future_competitions(self.comps)
        club['points'] = str(int(club['points']) + nb_places)
        self.comps[comp_id]['numberOfPlaces'] = str(int(self.comps[comp_id]['numberOfPlaces']) + nb_places)

        # On se déconnecte
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        template, context = captured_templates[3]
        assert template.name == 'index.html'
