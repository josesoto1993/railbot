import os
import time

from rail_utils.rail_utils import find_image_and_click, any_image_on_screen
from rail_utils.tabs_util import TAB_STATUS_DIR

RELOAD_LOOP_TIME = 15
RELOAD_MAX_TIME = 5 * 60
CHROME_RELOAD_BTN = "data/general/chrome_reload_btn.png"


def reload_web() -> bool:
    possible_states = [os.path.join(TAB_STATUS_DIR, filename) for filename in os.listdir(TAB_STATUS_DIR)]
    start_time = time.time()

    find_image_and_click([CHROME_RELOAD_BTN], msg="timetable")
    while time.time() - start_time < RELOAD_MAX_TIME:
        time.sleep(RELOAD_LOOP_TIME)
        on_screen, _, _, _ = any_image_on_screen(possible_states)
        if on_screen:
            return True
    return False
