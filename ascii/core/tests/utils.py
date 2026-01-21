import rest_framework.test

from ascii.users.tests.factories import AuthTokenFactory, UserFactory


class APITestCase(rest_framework.test.APITestCase):
    client: rest_framework.test.APIClient
    client_class: type[rest_framework.test.APIClient]

    def setUp(self) -> None:
        self.auth_user = UserFactory.create(is_staff=True)
        self.auth_token = AuthTokenFactory.create(user=self.auth_user)
        self.auth_client = self.client_class()
        self.auth_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.auth_token}")
