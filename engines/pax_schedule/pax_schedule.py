import datetime
import logging
import random

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, click_on_rect_area, sleep_random, any_image_on_screen, \
    get_screenshot, get_image_size, get_screenshot_with_black_box_in
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

TAB_ENGINE_FOLDER = "data/tab_engine"
PAX_ENGINE_HEADER_MAIN = TAB_ENGINE_FOLDER + "/paxengine_main.png"
PAX_ENGINE_HEADER_MAIN_SMALL = TAB_ENGINE_FOLDER + "/paxengine_main_small.png"
PAX_ENGINE_HEADER_HERMES = TAB_ENGINE_FOLDER + "/paxengine_hermes.png"
PAX_ENGINE_HEADER_HERMES_SMALL = TAB_ENGINE_FOLDER + "/paxengine_hermes_small.png"
PAX_ENGINE_HEADER_AJAX = TAB_ENGINE_FOLDER + "/paxengine_ajax.png"
PAX_ENGINE_HEADER_AJAX_SMALL = TAB_ENGINE_FOLDER + "/paxengine_ajax_small.png"
PAX_ENGINE_HEADER_KANGAROO = TAB_ENGINE_FOLDER + "/paxengine_kangaroo.png"
PAX_ENGINE_HEADER_KANGAROO_SMALL = TAB_ENGINE_FOLDER + "/paxengine_kangaroo_small.png"
PAX_ENGINE_HEADER_CHEETAH = TAB_ENGINE_FOLDER + "/paxengine_cheetah.png"
PAX_ENGINE_HEADER_CHEETAH_SMALL = TAB_ENGINE_FOLDER + "/paxengine_cheetah_small.png"
PAX_ENGINE_HEADER_GIRAFFE = TAB_ENGINE_FOLDER + "/paxengine_giraffe.png"
PAX_ENGINE_HEADER_GIRAFFE_SMALL = TAB_ENGINE_FOLDER + "/paxengine_giraffe_small.png"
PAX_ENGINE_HEADER_GREYHOUND = TAB_ENGINE_FOLDER + "/paxengine_greyhound.png"
PAX_ENGINE_HEADER_GREYHOUND_SMALL = TAB_ENGINE_FOLDER + "/paxengine_greyhound_small.png"
PAX_ENGINE_HEADER_WHALE = TAB_ENGINE_FOLDER + "/paxengine_whale.png"
PAX_ENGINE_HEADER_WHALE_SMALL = TAB_ENGINE_FOLDER + "/paxengine_whale_small.png"

ENGINE_FOLDER = "data/engine_schedule"
POPUP_TIMETABLE_BASE = ENGINE_FOLDER + "/popup_engine_timetable_calculator_base.png"
POPUP_TIMETABLE_BASE_SMALL = ENGINE_FOLDER + "/popup_engine_timetable_calculator_base_small.png"
POPUP_TIMETABLE_HOVER = ENGINE_FOLDER + "/popup_engine_timetable_calculator_hover.png"
POPUP_TIMETABLE_HOVER_SMALL = ENGINE_FOLDER + "/popup_engine_timetable_calculator_hover_small.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE = ENGINE_FOLDER + "/popup_engine_timetable_adopt_schedule_base.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE_SMALL = ENGINE_FOLDER + "/popup_engine_timetable_adopt_schedule_base_small.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER = ENGINE_FOLDER + "/popup_engine_timetable_adopt_schedule_hover.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER_SMALL = ENGINE_FOLDER + "/popup_engine_timetable_adopt_schedule_hover_small.png"
POPUP_TIMETABLE_KEEP_SCHEDULE_BASE = ENGINE_FOLDER + "/popup_engine_timetable_keep_schedule_base.png"
POPUP_TIMETABLE_KEEP_SCHEDULE_BASE_SMALL = ENGINE_FOLDER + "/popup_engine_timetable_keep_schedule_base_small.png"
POPUP_TIMETABLE_KEEP_SCHEDULE_HOVER = ENGINE_FOLDER + "/popup_engine_timetable_keep_schedule_hover.png"
POPUP_TIMETABLE_KEEP_SCHEDULE_HOVER_SMALL = ENGINE_FOLDER + "/popup_engine_timetable_keep_schedule_hover_small.png"
POPUP_SELECT_ALL_BASE = ENGINE_FOLDER + "/popup_engine_schedule_select_all_base.png"
POPUP_SELECT_ALL_BASE_SMALL = ENGINE_FOLDER + "/popup_engine_schedule_select_all_base_small.png"
POPUP_SELECT_ALL_HOVER = ENGINE_FOLDER + "/popup_engine_schedule_select_all_hover.png"
POPUP_SELECT_ALL_HOVER_SMALL = ENGINE_FOLDER + "/popup_engine_schedule_select_all_hover_small.png"
POPUP_SELECT_LETS_GO_BASE = ENGINE_FOLDER + "/popup_engine_schedule_lests_go_base.png"
POPUP_SELECT_LETS_GO_BASE_SMALL = ENGINE_FOLDER + "/popup_engine_schedule_lests_go_base_small.png"
POPUP_SELECT_LETS_GO_HOVER = ENGINE_FOLDER + "/popup_engine_schedule_lests_go_hover.png"
POPUP_SELECT_LETS_GO_HOVER_SMALL = ENGINE_FOLDER + "/popup_engine_schedule_lests_go_hover_small.png"
POPUP_SELECT_LETS_GO_DISABLED = ENGINE_FOLDER + "/popup_engine_schedule_lests_go_disabled.png"
POPUP_SELECT_LETS_GO_DISABLED_SMALL = ENGINE_FOLDER + "/popup_engine_schedule_lests_go_disabled_small.png"

logging.basicConfig(level=logging.INFO)


def get_top_schedule():
    schedule_labels = [POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE,
                       POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE_SMALL,
                       POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER,
                       POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER_SMALL,
                       POPUP_TIMETABLE_KEEP_SCHEDULE_BASE,
                       POPUP_TIMETABLE_KEEP_SCHEDULE_BASE_SMALL,
                       POPUP_TIMETABLE_KEEP_SCHEDULE_HOVER,
                       POPUP_TIMETABLE_KEEP_SCHEDULE_HOVER_SMALL]

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


class PaxSchedule(RailRunnable):
    def __init__(self, start_minute=5):
        self.next_run_time = datetime.datetime.now()
        self.start_minute = start_minute
        self.sleep_select_pax_engine = 10
        self.sleep_timetable = 10
        self.sleep_adopt_schedule = 20
        self.sleep_select_all = 30
        self.sleep_lets_go = 30

    def run(self) -> datetime:
        if self._should_run():
            self._run_pax_engine_schedule()
            self._update_next_run_time()
        return self.next_run_time

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_pax_engine_schedule(self):
        logging.info(f"----- Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()} -----")
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
        logging.info(f"----- Next {self.__class__.__name__} schedule at {target_datetime.time()} -----")

    def _select_pax_engine(self):
        pax_engine_headers = [PAX_ENGINE_HEADER_MAIN,
                              PAX_ENGINE_HEADER_MAIN_SMALL,
                              PAX_ENGINE_HEADER_HERMES,
                              PAX_ENGINE_HEADER_HERMES_SMALL,
                              PAX_ENGINE_HEADER_AJAX,
                              PAX_ENGINE_HEADER_AJAX_SMALL,
                              PAX_ENGINE_HEADER_KANGAROO,
                              PAX_ENGINE_HEADER_KANGAROO_SMALL,
                              PAX_ENGINE_HEADER_CHEETAH,
                              PAX_ENGINE_HEADER_CHEETAH_SMALL,
                              PAX_ENGINE_HEADER_GIRAFFE,
                              PAX_ENGINE_HEADER_GIRAFFE_SMALL,
                              PAX_ENGINE_HEADER_GREYHOUND,
                              PAX_ENGINE_HEADER_GREYHOUND_SMALL,
                              PAX_ENGINE_HEADER_WHALE,
                              PAX_ENGINE_HEADER_WHALE_SMALL]
        find_image_and_click(pax_engine_headers, msg="pax engine")
        sleep_random(self.sleep_select_pax_engine)

    def _open_timetable(self):
        popup_timetable = [POPUP_TIMETABLE_BASE,
                           POPUP_TIMETABLE_BASE_SMALL,
                           POPUP_TIMETABLE_HOVER,
                           POPUP_TIMETABLE_HOVER_SMALL]
        find_image_and_click(popup_timetable, msg="timetable")
        sleep_random(self.sleep_timetable)

    def _click_schedule(self):
        top_left_corner, image_path = get_top_schedule()
        click_on_rect_area(top_left_corner=top_left_corner, filepath=image_path)
        sleep_random(self.sleep_adopt_schedule)

    def _select_all_engines(self):
        select_all_btn = [POPUP_SELECT_ALL_BASE,
                          POPUP_SELECT_ALL_BASE_SMALL,
                          POPUP_SELECT_ALL_HOVER,
                          POPUP_SELECT_ALL_HOVER_SMALL]
        find_image_and_click(select_all_btn, msg="all engines")

        sleep_random(self.sleep_select_all)

    def _select_lets_go(self):
        lets_go_paths = [POPUP_SELECT_LETS_GO_BASE,
                         POPUP_SELECT_LETS_GO_BASE_SMALL,
                         POPUP_SELECT_LETS_GO_HOVER,
                         POPUP_SELECT_LETS_GO_HOVER_SMALL,
                         POPUP_SELECT_LETS_GO_DISABLED,
                         POPUP_SELECT_LETS_GO_DISABLED_SMALL]
        find_image_and_click(lets_go_paths, msg="lets go")
        sleep_random(self.sleep_lets_go)
