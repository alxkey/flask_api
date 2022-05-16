import psycopg2

from tokens import token_extraction


def try_catch(func):
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get all users DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get all users DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get all users DB: Error, {err}")
    return wrapper


def authorize(func):
    from controller import AuthController

    def wrapper(*args, **kwargs):
        token = token_extraction()
        auth = AuthController()
        authorized = auth.authorization(token)
        if authorized:
            ret = func(*args, **kwargs)
            return ret
        else:
            raise SystemError("Get user, authorization error")
    return wrapper
