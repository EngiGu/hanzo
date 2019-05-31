import os
from core.func import load_module

EXTRACT_LIST = load_module('lists', __file__, "List_")
EXTRACT_RESUME = load_module("resumes", __file__, "Resume_")

if __name__ == '__main__':
    print(EXTRACT_LIST)
    print(EXTRACT_RESUME)
    # ext = EXTRACT_RESUME.get("boss_cp")("")
    # ext.say_hello()
    pass
