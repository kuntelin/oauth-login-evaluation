from oauth_login_evaluation.auth.line.controller import LineAuthController


def get_line_auth_controller(line_config: object):
    return LineAuthController(line_config=line_config)
