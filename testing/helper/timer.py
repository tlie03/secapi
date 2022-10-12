import time


def timer(func):
    def wrapper(*args, **kwargs):
        t_start = time.time()
        ret = func(*args, **kwargs)
        t_end = time.time()
        print(f'{func} executed in: {t_end - t_start} seconds')
        return ret
    return wrapper