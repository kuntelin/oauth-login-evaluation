import httpx

from oauth_login_evaluation.auth import AuthInterface

__all__ = ["LocalAuthController"]


class LocalAuthController(AuthInterface):
    def __init__(self, line_config: object):
        self.jwt_secret = line_config.JWT_SECRET
        self.jwt_algorithm = line_config.JWT_ALGORITHM
        self.jwt_expiration = line_config.JWT_EXPIRATION

    def get_auth_url(self):
        params = {
            "response_type": "code",
            "client_id": self._channel_id,
            "redirect_uri": self._redirect_uri,
            "scope": self._scope,
            "state": self._generate_state(),
        }
        uri = "&".join([f"{k}={v}" for k, v in params.items()])

        return f"{self._sso_url}?{uri}"

    def get_token(self, code: str, *args, **kwargs):
        return {"access_token": "access"}

    def get_user_info(self, access_token):
        with httpx.Client() as client:
            print("fetching profile...")
            user_profile = client.get(
                self._profile_url,
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
            print(user_profile)

            return user_profile
