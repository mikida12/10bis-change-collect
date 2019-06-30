from functools import wraps
from time import sleep


def retry(tries=3, delay=5):
    def deco_retry(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            tried = 0
            result = False
            while tried < tries:
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    print(f"error! retrying in {delay} seconds")
                    # logger.exception(f"error! retrying in {delay} seconds")
                    sleep(delay)
                    tried += 1
            return result

        return func_retry

    return deco_retry
