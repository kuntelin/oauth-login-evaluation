from oauth_login_evaluation.auth.keycloak.controller import KeycloakAuthController


def get_keycloak_auth_controller(keycloak_config: object):
    return KeycloakAuthController(keycloak_config=keycloak_config)
