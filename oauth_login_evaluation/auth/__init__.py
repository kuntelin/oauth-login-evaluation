__all__ = [
    "AuthInterface",
]


class AuthInterface:
    def get_auth_url(self):
        raise NotImplementedError()

    def get_token(self, *args, **kwargs):
        raise NotImplementedError()

    def get_user_info(self, *args, **kwargs):
        raise NotImplementedError()
