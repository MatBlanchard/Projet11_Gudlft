from tests.unit_tests.conftest import clubs, competitions

class TestBook:

    clubs = clubs()
    comps = competitions()

    def test_valid_comp_and_valid_club_should_return_booking_page(self, client, captured_templates):
        club = self.clubs[0]
        comp = self.comps[0]
        response = client.get(f"/book/{comp['name']}/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "booking.html"

    def test_invalid_comp_and_valid_club_should_return_welcome_page(self, client, captured_templates):
        club = self.clubs[0]
        response = client.get(f"/book/invalid_comp/{club['name']}")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"

    def test_valid_comp_and_invalid_club_should_return_welcome_page(self, client, captured_templates):
        comp = self.comps[0]
        response = client.get(f"/book/{comp['name']}/invalid_club")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"

    def test_invalid_comp_and_invalid_club_should_return_welcome_page(self, client, captured_templates):
        response = client.get(f"/book/invalid_comp/invalid_club")
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
