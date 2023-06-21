import datetime
import logging
import random

from rail_utils.rail_utils import find_image_and_click, click_on_rect_area, sleep_random, any_image_on_screen, \
    get_screenshot, get_image_size, get_screenshot_with_black_box_in
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

PAX_ENGINE_HEADER_MAIN = "data/tab_engine/paxengine_main.png"
PAX_ENGINE_HEADER_AJAX = "data/tab_engine/paxengine_ajax.png"
PAX_ENGINE_HEADER_KANGAROO = "data/tab_engine/paxengine_kangaroo.png"
PAX_ENGINE_HEADER_CHEETAH = "data/tab_engine/paxengine_cheetah.png"
PAX_ENGINE_HEADER_GIRAFFE = "data/tab_engine/paxengine_giraffe.png"
PAX_ENGINE_HEADER_GREYHOUND = "data/tab_engine/paxengine_greyhound.png"
PAX_ENGINE_HEADER_WHALE = "data/tab_engine/paxengine_whale.png"
POPUP_TIMETABLE_BASE = "data/engine_schedule/popup_engine_timetable_calculator_base.png"
POPUP_TIMETABLE_HOVER = "data/engine_schedule/popup_engine_timetable_calculator_hover.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE = "data/engine_schedule/popup_engine_timetable_adopt_schedule_base.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER = "data/engine_schedule/popup_engine_timetable_adopt_schedule_hover.png"
POPUP_TIMETABLE_KEEP_SCHEDULE_BASE = "data/engine_schedule/popup_engine_timetable_keep_schedule_base.png"
POPUP_TIMETABLE_KEEP_SCHEDULE_HOVER = "data/engine_schedule/popup_engine_timetable_keep_schedule_hover.png"
POPUP_SELECT_ALL_BASE = "data/engine_schedule/popup_engine_schedule_select_all_base.png"
POPUP_SELECT_ALL_HOVER = "data/engine_schedule/popup_engine_schedule_select_all_hover.png"
POPUP_SELECT_LETS_GO_BASE = "data/engine_schedule/popup_engine_schedule_lests_go_base.png"
POPUP_SELECT_LETS_GO_HOVER = "data/engine_schedule/popup_engine_schedule_lests_go_hover.png"

logging.basicConfig(level=logging.INFO)


def get_top_schedule():
    schedule_labels = [POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE,
                       POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER,
                       POPUP_TIMETABLE_KEEP_SCHEDULE_BASE,
                       POPUP_TIMETABLE_KEEP_SCHEDULE_HOVER]

    matches = find_and_blackout_matches(schedule_labels)
    return select_top_schedule(matches)


def find_and_blackout_matches(schedule_labels):
    screenshot = get_screenshot()
    matches = []
    loop_counter = 1
    loop_limit = 100
    while True:
        on_screen, position, _, image_path = any_image_on_screen(
            paths_array=schedule_labels,
            screenshot=screenshot)

        if on_screen:
            matches.append((position, image_path))
            size = get_image_size(image_path)
            screenshot = get_screenshot_with_black_box_in(
                top_left_corner=position,
                size=size,
                screenshot=screenshot)
            loop_counter += 1
            if loop_counter > loop_limit:
                raise RuntimeError("Exceeded loop limit in _click_schedule function.")
        else:
            break
    return matches


def select_top_schedule(matches):
    # Sort the matches based on the y-coordinate (position[1]) in ascending order
    matches.sort(key=lambda match: match[0][1])
    # Select the match with the lowest y-coordinate (which is the first one in the sorted list)
    top_left_corner, image_path = matches[0]
    return top_left_corner, image_path


class PaxSchedule:
    def __init__(self, start_minute=5):
        self.next_run_time = datetime.datetime.now()
        self.start_minute = start_minute
        self.sleep_select_pax_engine = 10
        self.sleep_timetable = 10
        self.sleep_adopt_schedule = 20
        self.sleep_select_all = 30
        self.sleep_lets_go = 30

    def run(self):
        if self._should_run():
            try:
                self._run_pax_engine_schedule()
                self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_pax_engine_schedule(self):
        logging.info(f"----- Run pax engine schedule: Start at {datetime.datetime.now()} -----")
        open_tab(Tabs.ENGINES.value)
        self._select_pax_engine()
        self._open_timetable()
        self._click_schedule()
        self._select_all_engines()
        self._select_lets_go()

    def _update_next_run_time(self):
        current_datetime = datetime.datetime.now()
        target_hour = (current_datetime.hour + 1) % 24
        target_minute = random.randint(self.start_minute, self.start_minute + 10)
        if target_minute >= 60:
            target_minute = target_minute - 60
            target_hour = (target_hour + 1) % 24

        target_datetime = current_datetime.replace(hour=target_hour, minute=target_minute)

        if target_datetime < current_datetime:
            target_datetime += datetime.timedelta(days=1)

        self.next_run_time = target_datetime
        logging.info(f"----- Next run at {target_datetime.time()} -----")

    def _select_pax_engine(self):
        pax_engine_headers = [PAX_ENGINE_HEADER_MAIN,
                              PAX_ENGINE_HEADER_AJAX,
                              PAX_ENGINE_HEADER_KANGAROO,
                              PAX_ENGINE_HEADER_CHEETAH,
                              PAX_ENGINE_HEADER_GIRAFFE,
                              PAX_ENGINE_HEADER_GREYHOUND,
                              PAX_ENGINE_HEADER_WHALE]
        find_image_and_click(pax_engine_headers, msg="pax engine")
        sleep_random(self.sleep_select_pax_engine)

    def _open_timetable(self):
        find_image_and_click([POPUP_TIMETABLE_BASE, POPUP_TIMETABLE_HOVER], msg="timetable")
        sleep_random(self.sleep_timetable)

    def _click_schedule(self):
        top_left_corner, image_path = get_top_schedule()
        click_on_rect_area(top_left_corner=top_left_corner, filepath=image_path)
        sleep_random(self.sleep_adopt_schedule)

    def _select_all_engines(self):
        select_all_btn = [POPUP_SELECT_ALL_BASE, POPUP_SELECT_ALL_HOVER]
        find_image_and_click(select_all_btn, msg="all engines")

        sleep_random(self.sleep_select_all)

    def _select_lets_go(self):
        find_image_and_click([POPUP_SELECT_LETS_GO_BASE, POPUP_SELECT_LETS_GO_HOVER], msg="lets go")
        sleep_random(self.sleep_lets_go)
