from urllib.parse import quote_plus

from keycloak import KeycloakOpenID

from oauth_login_evaluation.auth import AuthInterface

__all__ = [
    "KeycloakAuthController",
]


class KeycloakAuthController(AuthInterface):
    def __init__(self, keycloak_config: object, *args, **kwargs):
        self._keycloak_config = keycloak_config
        self._keycloak_driver = KeycloakOpenID(
            server_url=self._keycloak_config.KEYCLOAK_SERVER_URL,
            realm_name=self._keycloak_config.KEYCLOAK_REALM,
            client_id=self._keycloak_config.KEYCLOAK_CLIENT_ID,
            client_secret_key=self._keycloak_config.KEYCLOAK_CLIENT_SECRET,
        )
        self._keycloak_driver.well_known()

    def get_auth_url(self):
        scope = "profile%20openid%20email"
        redirect_uri = self._keycloak_config.KEYCLOAK_REDIRECT_URI

        return self._keycloak_driver.auth_url(
            scope=scope,
            redirect_uri=quote_plus(redirect_uri),
        )

    def get_token(self, *args, **kwargs):
        return self._keycloak_driver.token(*args, **kwargs)

    def get_user_info(self, *args, access_token: str = None, **kwargs):
        return self._keycloak_driver.userinfo(access_token)
