import time
from loguru import logger
from os.path import abspath, dirname

# Absolute directory path
PROJECT_PATH = abspath(dirname(__file__))


def timeit(method):
    """
    Show time elapsed when decorating with @timeit
    """
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        finish_time = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((finish_time - start_time))
        else:
            try:
                elapsed_time = finish_time - start_time
                logger.info(f'{method.__name__} run time: {time_format(int(elapsed_time))}')
            except Exception:
                logger.error('%r run time: %s' % (method.__name__, time_format(int(finish_time - start_time))))
        return result

    return timed


def time_format(seconds: int):
    "Convert seconds to time format"
    if seconds is not None:
        seconds = int(seconds)
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if d > 0:
            return '{:02d}D {:02d}H {:02d}m {:02d}s'.format(d, h, m, s)
        elif h > 0:
            return '{:02d}H {:02d}m {:02d}s'.format(h, m, s)
        elif m > 0:
            return '{:02d}m {:02d}s'.format(m, s)
        elif s > 0:
            return '{:02d}s'.format(s)
    return '-'


def confirm_prompt() -> bool:
    """
    Yes promp for methods
    """
    reply = None
    while reply not in ("", "y", "n"):
        reply = input(f"Are you sure? (Y/n): \n").lower()
    return reply in ("", "y")
