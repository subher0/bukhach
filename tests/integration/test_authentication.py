import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

from bukhach.models.profile_models import Profile


class AuthenticationTest(TestCase):
    client = Client()

    def setUp(self):
        pass

    def test_auth(self):
        self.user = User.objects.create_user(username='imgay', first_name='im', last_name='gay', email='im@g.ay', password='gayyy')
        response = self.client.post('/api/v1/token-auth/', {'username': 'imgay', 'password': 'gayyy'})

        assert response.status_code == 200
        assert response.json()['token'] is not None

    def test_registration(self):
        self.client.post('/api/v1/profile', json.dumps({'tel_num':'88888888888', 'user': {'username': 'imgay', 'email': 'im@g.ay',
                                                       'first_name': 'im', 'last_name': 'gay', 'password': 'gayyy'}}),
                                    content_type='application/json')
        token = self.client.post('/api/v1/token-auth/', {'username': 'imgay', 'password': 'gayyy'}).json()['token']

        response = self.client.get('/api/v1/profile', HTTP_AUTHORIZATION='JWT ' + token)

        assert response.status_code == 200
        assert response.json()['username'] == 'imgay'


    def tearDown(self):
        pass