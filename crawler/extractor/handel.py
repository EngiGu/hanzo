import os
from core.func import load_module


EXTRACT_LIST = load_module(os.path.join(os.path.dirname(__file__), "lists"), "List_")
EXTRACT_RESUME = load_module(os.path.join(os.path.dirname(__file__), "resumes"), "Resume_")



if __name__ == '__main__':
    print(EXTRACT_LIST)
    print(EXTRACT_RESUME)
    # ext = EXTRACT_RESUME.get("boss_cp")("")
    # ext.say_hello()
    pass