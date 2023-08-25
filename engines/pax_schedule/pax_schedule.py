import datetime
import logging
import random

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, click_on_rect_area, sleep_random, any_image_on_screen, \
    get_screenshot, get_image_size, get_screenshot_with_black_box_in, get_image_paths_from_folder
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

TAB_ENGINE_FOLDER = "data/tab_engine"
PAX_ENGINE_FILES = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/engines_label")
PAX_ENGINE_FILES.sort(key=lambda x: ("main" not in x, x))

ENGINE_FOLDER = "data/engine_schedule"
POPUP_TIMETABLE_BTN_FOLDER = ENGINE_FOLDER + "/timetable_btn"
POPUP_TIMETABLE_KEEP_FOLDER = ENGINE_FOLDER + "/timetable_keep"
POPUP_TIMETABLE_ADOPT_FOLDER = ENGINE_FOLDER + "/timetable_adopt"
POPUP_SELECT_ALL_FOLDER = ENGINE_FOLDER + "/select_all"
POPUP_SELECT_LETS_GO_FOLDER = ENGINE_FOLDER + "/letsgo"

logging.basicConfig(level=logging.INFO)


def get_top_schedule():
    schedule_labels = (
            get_image_paths_from_folder(POPUP_TIMETABLE_ADOPT_FOLDER) +
            get_image_paths_from_folder(POPUP_TIMETABLE_KEEP_FOLDER)
    )

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
        logging.info(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
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
        logging.info(f"Next {self.__class__.__name__} schedule at {target_datetime.time()}")

    def _select_pax_engine(self):
        find_image_and_click(PAX_ENGINE_FILES, msg="pax engine")
        sleep_random(self.sleep_select_pax_engine)

    def _open_timetable(self):
        popup_timetable = get_image_paths_from_folder(POPUP_TIMETABLE_BTN_FOLDER)
        find_image_and_click(popup_timetable, msg="timetable")
        sleep_random(self.sleep_timetable)

    def _click_schedule(self):
        top_left_corner, image_path = get_top_schedule()
        click_on_rect_area(top_left_corner=top_left_corner, filepath=image_path)
        sleep_random(self.sleep_adopt_schedule)

    def _select_all_engines(self):
        select_all_btn = get_image_paths_from_folder(POPUP_SELECT_ALL_FOLDER)
        find_image_and_click(select_all_btn, msg="all engines")

        sleep_random(self.sleep_select_all)

    def _select_lets_go(self):
        lets_go_paths = get_image_paths_from_folder(POPUP_SELECT_LETS_GO_FOLDER)
        find_image_and_click(lets_go_paths, msg="lets go")
        sleep_random(self.sleep_lets_go)
