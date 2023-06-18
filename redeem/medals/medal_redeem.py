import datetime
import logging

from rail_utils.rail_utils import image_on_screen, find_image_and_click, sleep_random
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

MEDAL_REDEEM_MINUTES_TO_RECHECK = 120
MEDAL_REDEEM_LABEL = "data/tab_medal/redeem_label.png"

logging.basicConfig(level=logging.INFO)


class MedalRedeem:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_redeem_all = 5

    def run(self):
        if self._should_run():
            try:
                self._run_medal_redeem()
                self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_medal_redeem(self):
        logging.info(f"----- Run medal redeem: Start at {datetime.datetime.now()} -----")
        open_tab(Tabs.MEDALS)
        self._redeem_all()

    def _redeem_all(self):
        redeem_label_on_screen, _, _ = image_on_screen(MEDAL_REDEEM_LABEL)

        if not redeem_label_on_screen:
            logging.info("No medal to redeem")
            return

        while redeem_label_on_screen:
            find_image_and_click([MEDAL_REDEEM_LABEL], msg="redeem medal")
            sleep_random(self.sleep_redeem_all)
            redeem_label_on_screen, _, _ = image_on_screen(MEDAL_REDEEM_LABEL)

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=MEDAL_REDEEM_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next medal redeem check at {target_datetime.time()} -----")
