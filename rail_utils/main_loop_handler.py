import datetime
import logging
import time
from typing import List, Optional

from rail_utils.rail_runnable import RailRunnable
from rail_utils.web_utils import reload_web

ERRORS_TO_RELOAD = 10


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
