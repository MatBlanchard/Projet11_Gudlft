from tests.conftest import clubs, competitions


class TestPointsDisplay:

    clubs = clubs()
    comps = competitions()

    def test_points_display_route_should_return_points_display_page(self, client, captured_templates):
        response = client.get('/points_display')
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'points_display.html'
        assert context['clubs'] == self.clubs