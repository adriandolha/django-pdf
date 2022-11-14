from django.test import Client


class TestHealth:
    def test_health_valid(self):
        client = Client()
        response = client.get('/health/')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'OK'
