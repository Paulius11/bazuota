import time
from loguru import logger
from os.path import abspath, dirname
import  os

# Absolute directory path
PROJECT_PATH = abspath(dirname(__file__))

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
RUNNER_PATH = os.getcwd()

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

def single_yes_or_no_question(question, default_no=True):
    "Simple question for yes no"
    choices = ' [y/N]: ' if default_no else ' [Y/n]: '
    default_answer = 'n' if default_no else 'y'
    reply = str(input(question + choices)).lower().strip() or default_answer
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False if default_no else True

class Open(object):
    """
    Contect manger for opening files

    with Open('pancake-LP-abi') as f:
        pancake_LP_ABI = f
    """
    def __init__(self, file_name):
        try:
            self.file_path = file_name
            self.file_obj = open(self.file_path, 'r').read()
        except FileNotFoundError:
            try:
                self.file_path = os.path.join(RUNNER_PATH, file_name)
                self.file_obj = open(self.file_path, 'r').read()
            except FileNotFoundError:
                self.file_path = os.path.join(THIS_PATH, file_name)
                self.file_obj = open(self.file_path, 'r').read()

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        logger.info(f"file loaded: {self.file_path}")

