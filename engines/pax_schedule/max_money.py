import datetime
import logging
import random

from rail_utils.rail_utils import find_image_and_click, click_on_rect_area, sleep_random
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

PAX_ENGINE_HEADER = "data/tab_engine/paxengine_main.png"
POPUP_TIMETABLE_BASE = "data/engine_schedule/popup_engine_timetable_calculator_base.png"
POPUP_TIMETABLE_HOVER = "data/engine_schedule/popup_engine_timetable_calculator_hover.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE = "data/engine_schedule/popup_engine_timetable_adopt_schedule_base.png"
POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER = "data/engine_schedule/popup_engine_timetable_adopt_schedule_hover.png"
POPUP_SELECT_ALL_BASE = "data/engine_schedule/popup_engine_schedule_select_all_base.png"
POPUP_SELECT_ALL_HOVER = "data/engine_schedule/popup_engine_schedule_select_all_hover.png"
POPUP_SELECT_LETS_GO_BASE = "data/engine_schedule/popup_engine_schedule_lests_go_base.png"
POPUP_SELECT_LETS_GO_HOVER = "data/engine_schedule/popup_engine_schedule_lests_go_hover.png"

logging.basicConfig(level=logging.INFO)


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
        logging.info(f"----- Run pax engine schedule: Start -----")
        open_tab(Tabs.ENGINES)
        self._select_pax_engine()
        self._open_timetable()
        self._open_adopt_schedule()
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
        find_image_and_click([PAX_ENGINE_HEADER], msg="pax engine")
        sleep_random(self.sleep_select_pax_engine)

    def _open_timetable(self):
        find_image_and_click([POPUP_TIMETABLE_BASE, POPUP_TIMETABLE_HOVER], msg="timetable")
        sleep_random(self.sleep_timetable)

    def _open_adopt_schedule(self):
        find_image_and_click([POPUP_TIMETABLE_ADOPT_SCHEDULE_BASE, POPUP_TIMETABLE_ADOPT_SCHEDULE_HOVER],
                             msg="adopt schedule")
        sleep_random(self.sleep_adopt_schedule)

    def _select_all_engines(self):
        # TODO: use the function, not the hardcoded
        # find_image_and_click([POPUP_SELECT_ALL_BASE, POPUP_SELECT_ALL_HOVER],
        #                       on_screen_msg="Select all engines",
        #                       on_fail_msg="Fail select all engines",
        #                       precision=0.8)
        click_on_rect_area(top_left_corner=(250, 500), size=(25, 25))
        sleep_random(self.sleep_select_all)
        # ENDTODO

    def _select_lets_go(self):
        find_image_and_click([POPUP_SELECT_LETS_GO_BASE, POPUP_SELECT_LETS_GO_HOVER], msg="lets go")
        sleep_random(self.sleep_lets_go)
