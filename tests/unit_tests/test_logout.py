class TestLogout:

    def test_logout_route_should_return_index_page(self, client, captured_templates):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == 'index.html'
