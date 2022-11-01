import os
from datetime import datetime

from clear_catalog import clear_catalog

SRC = './tmp_files/'
clear_time = '142700'


# чистка папки назначения
def clear_src():
    clear_catalog(SRC)
    if not os.path.exists(SRC):
        os.makedirs(SRC)


def run_clear():
    while 5 < 6:
        if datetime.now().strftime("%H%M%S") == clear_time:
            clear_src()
