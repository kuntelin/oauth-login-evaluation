import os

# * settings for logging
VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
TRACING = os.getenv("TRACING", "false").lower() == "true"

# * settings for the application
# JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION = os.getenv("JWT_EXPIRATION", 3600)

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", None)
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", None)
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", None)
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", None)
KEYCLOAK_REDIRECT_URI = os.getenv("KEYCLOAK_REDIRECT_URI", None)

LINE_LOGIN_URL = "https://access.line.me/oauth2/v2.1/authorize?"
LINE_LOGIN_CHANNEL_ID = os.getenv("LINE_LOGIN_CHANNEL_ID", "")
LINE_LOGIN_CHANNEL_SECRET = os.getenv("LINE_LOGIN_CHANNEL_SECRET", "")
LINE_LOGIN_REDIRECT_URI = os.getenv("LINE_LOGIN_REDIRECT_URI", "")

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./oauth_login_evaluation.db")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/oauth-login-evaluation")
