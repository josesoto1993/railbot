import datetime
import logging
import os
import time
from typing import List, Optional

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import any_image_on_screen, find_image_and_click
from rail_utils.tabs_util import TAB_STATUS_DIR

RELOAD_LOOP_TIME = 15

RELOAD_MAX_TIME = 5 * 60
ERRORS_TO_RELOAD = 10
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


class MainLoopHandler:
    def __init__(self, tasks: List[RailRunnable]):
        self.tasks = tasks
        self.next_run_times = {task.__class__.__name__: datetime.datetime.now() for task in self.tasks}
        self.error_counter = 0

    def main_loop(self):
        while True:
            for task in self.tasks:
                next_time = self._run_single_task(task)
                if next_time is not None:
                    self.next_run_times[task.__class__.__name__] = next_time
            self._sleep_till_next_loop()

    def _sleep_till_next_loop(self):
        now = datetime.datetime.now()
        min_task, min_time = min(self.next_run_times.items(), key=lambda x: x[1])
        raw_seconds = (min_time - now).total_seconds()
        seconds = max(0.0, raw_seconds)
        logging.info(f"Next run for {min_task} in {seconds} seconds at {min_time.time()}")
        time.sleep(seconds)

    def _run_single_task(self, task: RailRunnable) -> Optional[datetime]:
        try:
            return task.run()
        except Exception as e:
            self.error_counter += 1
            logging.error(str(e))
            if self.error_counter >= ERRORS_TO_RELOAD:
                reload = reload_web()
                if reload:
                    self.error_counter = 0
        return None
