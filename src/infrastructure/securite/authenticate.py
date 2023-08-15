from backend.src.infrastructure.configuration.application_configuration import ApplicationConfiguration

user_service = ApplicationConfiguration().get_user_service()


def authenticate(login, password):
    login_user = user_service.login_user(login, password)

    return login_user
