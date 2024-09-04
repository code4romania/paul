from django.conf import settings
from django.test import Client, TestCase


class SignupTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST=settings.ALLOWED_HOSTS[0])

    def test_disabled_public_signup(self):
        response = self.client.post(
            "/api/auth/users/",
            {
                "email": "test1@example.com",
                "password": "OneTestPass1",
                "re_password": "OneTestPass1",
                "username": "test1@example.com",
            },
        )
        self.assertEqual(response.status_code, 401)
