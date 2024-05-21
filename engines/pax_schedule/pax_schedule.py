import datetime
import logging
import random

from rail_utils.folders_paths import ENGINE_FOLDER, TAB_ENGINE_FOLDER, ERROR_FOLDER
from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, click_on_rect_area, sleep_random, any_image_on_screen, \
    get_screenshot, get_image_size, get_screenshot_with_black_box_in, get_image_paths_from_folder, \
    ImageNotFoundException
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

RANDOM_MINUTES_TO_ADD = 10
NEXT_RUN_MIN_POSSIBLE_SECONDS = 30 * 60
NEXT_RUN_MAX_POSSIBLE_SECONDS = 90 * 60

logging.basicConfig(level=logging.INFO)


def get_top_schedule():
    popup_timetable_adopt_or_keep_files = (
            get_image_paths_from_folder(ENGINE_FOLDER + "/timetable_adopt") +
            get_image_paths_from_folder(ENGINE_FOLDER + "/timetable_keep")
    )
    matches = find_and_blackout_matches(popup_timetable_adopt_or_keep_files)
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
    # There should be matches, otherwise is an error
    if not matches:
        get_screenshot(save=True, filename=f"{ERROR_FOLDER}/cant_find_timetable_adopt_or_keep")
        raise ImageNotFoundException("Cant find timetable adopt or keep")

    # Sort the matches based on the y-coordinate (position[1]) in ascending order
    matches.sort(key=lambda match: match[0][1])
    # Select the match with the lowest y-coordinate (which is the first one in the sorted list)
    top_left_corner, image_path = matches[0]
    return top_left_corner, image_path


def adjust_target_time(current_datetime, target_minute):
    target_datetime = current_datetime.replace(minute=target_minute)

    time_difference = target_datetime - current_datetime
    while not (NEXT_RUN_MIN_POSSIBLE_SECONDS <= time_difference.total_seconds() <= NEXT_RUN_MAX_POSSIBLE_SECONDS):
        if time_difference.total_seconds() < NEXT_RUN_MIN_POSSIBLE_SECONDS:
            target_datetime += datetime.timedelta(hours=1)
        elif time_difference.total_seconds() > NEXT_RUN_MAX_POSSIBLE_SECONDS:
            target_datetime -= datetime.timedelta(hours=1)

        time_difference = target_datetime - current_datetime
    return target_datetime


class PaxSchedule(RailRunnable):
    def __init__(self, start_minute=5):
        super().__init__()
        self.task_name = self.__class__.__name__
        self.start_minute = start_minute
        self.sleep_select_pax_engine = 10
        self.sleep_timetable = 10
        self.sleep_adopt_schedule = 20
        self.sleep_select_all = 30
        self.sleep_lets_go = 30

    def _run(self):
        self._run_pax_engine_schedule()

    def _update_next_run_time(self):
        current_datetime = datetime.datetime.now()
        target_minute = random.randint(self.start_minute, self.start_minute + RANDOM_MINUTES_TO_ADD) % 60
        target_datetime = adjust_target_time(current_datetime, target_minute)

        self.next_run_time = target_datetime
        logging.debug(f"Next {self.__class__.__name__} schedule at {target_datetime.time()}")

    def _run_pax_engine_schedule(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.ENGINES.value)
        self._select_pax_engine()
        self._open_timetable()
        self._click_schedule()
        self._select_all_engines()
        self._select_lets_go()

    def _select_pax_engine(self):
        pax_engine_files = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/engines_label")
        pax_engine_files.sort(key=lambda x: ("main" not in x, x))
        find_image_and_click(pax_engine_files,
                             msg="pax engine",
                             error_filename="fail_select_pax_engine")
        sleep_random(self.sleep_select_pax_engine)

    def _open_timetable(self):
        popup_timetable_btn_files = get_image_paths_from_folder(ENGINE_FOLDER + "/timetable_btn")
        find_image_and_click(popup_timetable_btn_files,
                             msg="timetable",
                             error_filename="fail_open_timetable")
        sleep_random(self.sleep_timetable)

    def _click_schedule(self):
        top_left_corner, image_path = get_top_schedule()
        click_on_rect_area(top_left_corner=top_left_corner, filepath=image_path)
        sleep_random(self.sleep_adopt_schedule)

    def _select_all_engines(self):
        popup_select_all_files = get_image_paths_from_folder(ENGINE_FOLDER + "/select_all")
        find_image_and_click(popup_select_all_files,
                             msg="all engines",
                             error_filename="fail_select_all_engines")
        sleep_random(self.sleep_select_all)

    def _select_lets_go(self):
        popup_select_lets_go_files = get_image_paths_from_folder(ENGINE_FOLDER + "/letsgo")
        find_image_and_click(popup_select_lets_go_files,
                             msg="lets go",
                             error_filename="fail_select_lets_go")
        sleep_random(self.sleep_lets_go)
