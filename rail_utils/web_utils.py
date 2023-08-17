import logging
import os
import time

from rail_utils.rail_utils import find_image_and_click, any_image_on_screen, close_all_pop_ups
from rail_utils.tabs_util import TAB_STATUS_DIR

RELOAD_LOOP_TIME = 15
RELOAD_MAX_TIME = 5 * 60
CHROME_RELOAD_BTN = "data/general/chrome_reload_btn.png"

logging.root.setLevel(logging.INFO)


def reload_web() -> bool:
    possible_states = [os.path.join(TAB_STATUS_DIR, filename) for filename in os.listdir(TAB_STATUS_DIR)]
    start_time = time.time()

    find_image_and_click([CHROME_RELOAD_BTN], msg="reload btn")
    while time.time() - start_time < RELOAD_MAX_TIME:
        time.sleep(RELOAD_LOOP_TIME)
        on_screen, _, _, _ = any_image_on_screen(possible_states)
        if on_screen:
            try:
                close_all_pop_ups()
            except Exception as e:
                logging.error(str(e))
            return True
    return False
