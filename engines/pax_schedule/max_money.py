import logging
import random
import time

from engines.engines_general_util import open_engines_tab
from rail_utils.rail_utils import move_mouse_to_center, wait_rail_response, image_on_screen, find_image_and_click, \
    click_on_rect_area

PAX_ENGINE_HEADER = "data/tab_engine/enginename_hades.png"
POPUP_TIMETABLE_BASE = "data/engine_schedule/popup_engine_timetable_calculator_base.png"
POPUP_TIMETABLE_HOVER = "data/engine_schedule/popup_engine_timetable_calculator_hover.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE = "data/engine_schedule/popup_engine_timetable_adopt_schedule_base.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER = "data/engine_schedule/popup_engine_timetable_adopt_schedule_hover.png"
POPUP_SELECT_ALL_BASE = "data/engine_schedule/popup_engine_schedule_select_all_base.png"
POPUP_SELECT_ALL_HOVER = "data/engine_schedule/popup_engine_schedule_select_all_hover.png"
POPUP_SELECT_LETS_GO_BASE = "data/engine_schedule/popup_engine_schedule_lests_go_base.png"
POPUP_SELECT_LETS_GO_HOVER = "data/engine_schedule/popup_engine_schedule_lests_go_hover.png"

logging.basicConfig(level=logging.INFO)


def set_schedule():
    try:
        move_mouse_to_center()
        wait_rail_response()
        open_engines_tab()
        find_image_and_click([PAX_ENGINE_HEADER],
                             on_screen_msg="Open pax engine",
                             on_fail_msg="Fail open pax engine")
        find_image_and_click([POPUP_TIMETABLE_BASE, POPUP_TIMETABLE_HOVER],
                             on_screen_msg="Open timetable",
                             on_fail_msg="Fail open timetable")
        find_image_and_click([POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE, POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER],
                             on_screen_msg="Open adopt schedule",
                             on_fail_msg="Fail open adopt schedule")
        # TODO: use the function, not the hardcoded
        # find_image_and_click([POPUP_SELECT_ALL_BASE, POPUP_SELECT_ALL_HOVER], on_screen_msg="Select all engines", on_fail_msg="Fail select all engines", precision=0.8)
        time.sleep(random.uniform(20, 30))
        click_on_rect_area(top_left_corner=(250, 500), size=(25, 25))
        time.sleep(random.uniform(30, 45))
        # ENDTODO
        find_image_and_click([POPUP_SELECT_LETS_GO_BASE, POPUP_SELECT_LETS_GO_HOVER],
                             on_screen_msg="Select lets go",
                             on_fail_msg="Fail select lets go")
    except Exception as exception:
        logging.error(str(exception))
        return


def check_finish_load_engine_tab():
    on_screen, _ = image_on_screen("data/tabs/tab_header_engine.png", precision=0.99)
    return on_screen
