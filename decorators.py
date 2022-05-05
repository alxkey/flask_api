import psycopg2

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

