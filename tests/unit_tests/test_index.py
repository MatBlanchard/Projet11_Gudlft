class TestIndex:

    def test_index_route_should_return_index_page(self, client, captured_templates):
        response = client.get('/')
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'index.html'