from ascii.users.tests.factories import AuthTokenFactory


def test_auth_token_generate_key():
    """
    The key should be generated on the initial model save().
    """
    token = AuthTokenFactory.create()
    assert token.key
