import httpx

from oauth_login_evaluation.auth import AuthInterface

__all__ = ["LineAuthController"]


class LineAuthController(AuthInterface):
    def __init__(self, line_config: object):
        self._channel_id = line_config.LINE_LOGIN_CHANNEL_ID
        self._channel_secret = line_config.LINE_LOGIN_CHANNEL_SECRET
        self._redirect_uri = line_config.LINE_LOGIN_REDIRECT_URI
        self._grant_type = "authorization_code"
        self._scope = "profile openid email"

        self._sso_url = "https://access.line.me/oauth2/v2.1/authorize"
        self._token_url = "https://api.line.me/oauth2/v2.1/token"
        self._profile_url = "https://api.line.me/v2/profile"

    def _generate_state(self, length=10):
        import random
        import string

        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_auth_url(self):
        params = {
            "response_type": "code",
            "client_id": self._channel_id,
            "redirect_uri": self._redirect_uri,
            "scope": self._scope,
            "state": self._generate_state(),
            "user_id": "bc5af780c6fb473790ac1c0e764d6165",
        }
        uri = "&".join([f"{k}={v}" for k, v in params.items()])

        return f"{self._sso_url}?{uri}"

    def get_token(self, code: str, *args, **kwargs):
        with httpx.Client() as client:
            print("fetching token...")
            token = client.post(
                self._token_url,
                data={
                    "client_id": self._channel_id,
                    "client_secret": self._channel_secret,
                    "redirect_uri": self._redirect_uri,
                    "grant_type": self._grant_type,
                    "code": code,
                },
            ).json()
            print(token)

            return token

    def get_user_info(self, access_token):
        with httpx.Client() as client:
            print("fetching profile...")
            user_profile = client.get(
                self._profile_url,
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
            print(user_profile)

            return user_profile
