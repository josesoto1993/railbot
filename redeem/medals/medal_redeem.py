import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, sleep_random, any_image_on_screen
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

MEDAL_REDEEM_MINUTES_TO_RECHECK = 120

MEDAL_REDEEM_LABEL = "data/tab_medal/redeem_label.png"
MEDAL_REDEEM_LABEL_SMALL = "data/tab_medal/redeem_label_small.png"
REDEEM_MEDAL_LABEL = [MEDAL_REDEEM_LABEL, MEDAL_REDEEM_LABEL_SMALL]

logging.basicConfig(level=logging.INFO)


class MedalRedeem(RailRunnable):
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_redeem_all = 5

    def run(self) -> datetime:
        if self._should_run():
            self._run_medal_redeem()
            self._update_next_run_time()
        return self.next_run_time

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_medal_redeem(self):
        logging.info(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.MEDALS.value)
        self._redeem_all()

    def _redeem_all(self):
        on_screen, _, _, _ = any_image_on_screen(REDEEM_MEDAL_LABEL)

        if not on_screen:
            logging.debug("No medal to redeem")
            return

        while on_screen:
            find_image_and_click(REDEEM_MEDAL_LABEL, msg="redeem medal")
            sleep_random(self.sleep_redeem_all)
            on_screen, _, _, _ = any_image_on_screen(REDEEM_MEDAL_LABEL)

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=MEDAL_REDEEM_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"Next {self.__class__.__name__} check at {target_datetime.time()}")
