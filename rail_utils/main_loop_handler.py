import datetime
import logging
import time
from typing import List, Optional

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import count_down
from rail_utils.web_utils import reload_web

WAIT_HUMAN_CHECK_ERROR = 180

ERRORS_TO_RELOAD = 10

logging.root.setLevel(logging.INFO)


class MainLoopHandler:
    def __init__(self, tasks: List[RailRunnable], enable_count_down=False):
        self.count = 0
        self.tasks = tasks
        self.next_run_times = {task.__class__.__name__: datetime.datetime.now() for task in self.tasks}
        self.error_counter = 0
        self.enable_count_down = enable_count_down

    def start(self):
        while True:
            if self.enable_count_down:
                count_down()
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
        logging.info(f"----- Next run for {min_task} in {seconds} seconds at {min_time.time()} -----")
        time.sleep(seconds)

    def _run_single_task(self, task: RailRunnable) -> Optional[datetime]:
        try:
            return task.handle_run()
        except Exception as e:
            self._handle_run_exception(e)

        return None

    def _handle_run_exception(self, e):
        self.error_counter += 1
        logging.error(str(e))
        self._reload_if_needed()
        self._wait_human_check_error()

    def _reload_if_needed(self):
        if self.error_counter >= ERRORS_TO_RELOAD:
            try:
                reload_web()
                logging.info(f"Run reload: Start at {datetime.datetime.now().time()}")
            except Exception as e:
                logging.error(f"Run reload: error -> {e}")
            finally:
                self.error_counter = 0
        else:
            logging.info(f"No need reload, as {self.error_counter} errors is less than {ERRORS_TO_RELOAD}")

    def _wait_human_check_error(self):
        if self.enable_count_down:
            count_down()
            logging.info(f"Wait {WAIT_HUMAN_CHECK_ERROR} seconds to let an human check the error")
            time.sleep(WAIT_HUMAN_CHECK_ERROR)
        else:
            logging.info("Human check wait disabled")
