import datetime
import logging
from abc import ABC, abstractmethod
from typing import Optional


class RailRunnable(ABC):
    def __init__(self):
        self.count = 0
        self.task_name = "undefined"
        self.next_run_time = datetime.datetime.now()

    def handle_run(self) -> Optional[datetime]:
        if self._should_run():
            self._run()
            self._update_next_run_time()
            self._print_and_update_count()
        return self.next_run_time

    @abstractmethod
    def _run(self) -> None:
        pass

    @abstractmethod
    def _update_next_run_time(self) -> None:
        pass

    def _should_run(self) -> bool:
        return datetime.datetime.now() >= self.next_run_time

    def _print_and_update_count(self):
        self.count += 1
        logging.info(f"Total runs for {self.task_name} = {self.count}")
