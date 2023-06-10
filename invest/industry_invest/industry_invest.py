import datetime
import logging

from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab


class IndustryInvest:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()

    def invest(self):
        if self._should_run():
            try:
                invest_done = self._run_invest()
                if invest_done:
                    logging.info(f"----- May have more industries to invest, next loop invest another one -----")
                else:
                    self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_invest(self):
        logging.info(f"----- Run industry invest: Start -----")
        open_tab(Tabs.RANKINGS)

        return True

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=30)

        self.next_run_time = target_datetime
        logging.info(f"----- Next industry invest at {target_datetime.time()} -----")
