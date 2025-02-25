# OAuth Login Evaluation

## Environment Variables

### Example

```dotenv
# * app
VERBOSE=false
DEBUG=false
TRACING=false
JWT_SECRET=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
DATABASE_URL=postgresql://user:password@localhost:5432/oauth-login-evaluation

# * keycloak
KEYCLOAK_SERVER_URL=http://localhost:8080/auth
KEYCLOAK_REALM=oauth-login-evaluation
KEYCLOAK_CLIENT_ID=oauth-login-evaluation
KEYCLOAK_CLIENT_SECRET=
KEYCLOAK_REDIRECT_URI=http://localhost:8000/auth/keycloak/callback

# * line
LINE_LOGIN_CHANNEL_ID=
LINE_LOGIN_CHANNEL_SECRET=7ea7c34ec9da11d5e02b72639cffb5a
LINE_LOGIN_REDIRECT_URI=http://localhost:8000/auth/line/callback

```

### JWT_SECRET

JWT_SECRET should be a long random string

You can generate one using:

```shell
openssl rand -hex 32
```

## Keycloak setting

### Setup REALM and Client

1. Open `http://localhost:8080` in Browser
2. Sign-in with admin / admin
3. Create a new "REALM"
4. Update "REALM" setting
   1. "General" -> "Require SSL" -> "None"
   2. "Themes" -> "Login theme" -> "keycloak"
   3. "Themes" -> "Account theme" -> "keycloak.v3"
5. Create new client
   1. Enable "Client authentication"
   2. Enable "Authentication flow" -> "Standard flow"
6. Update client setting
   1. "Settings" -> "Valid redirect URIs" -> add "*"
7. Add new user
8. Update user credential
   1. "Credentials" -> "Set password"
   2. Disable "Temporary"
