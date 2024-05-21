import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, sleep_random, any_image_on_screen, get_image_paths_from_folder
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

MEDAL_REDEEM_MINUTES_TO_RECHECK = 120

REDEEM_MEDAL_LABEL_FILES = get_image_paths_from_folder("data/tab_medal/redeem")

logging.basicConfig(level=logging.INFO)


class MedalRedeem(RailRunnable):

    def __init__(self):
        super().__init__()
        self.task_name = self.__class__.__name__
        self.next_run_time = datetime.datetime.now()
        self.sleep_redeem_all = 5

    def _run(self):
        self._run_medal_redeem()

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=MEDAL_REDEEM_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.debug(f"Next {self.__class__.__name__} check at {target_datetime.time()}")

    def _run_medal_redeem(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.MEDALS.value)
        self._redeem_all()

    def _redeem_all(self):
        on_screen, _, _, _ = any_image_on_screen(REDEEM_MEDAL_LABEL_FILES)

        if not on_screen:
            logging.debug("No medal to redeem")
            return

        while on_screen:
            find_image_and_click(REDEEM_MEDAL_LABEL_FILES,
                                 msg="redeem medal",
                                 error_filename="fail_redeem_all")
            sleep_random(self.sleep_redeem_all)
            on_screen, _, _, _ = any_image_on_screen(REDEEM_MEDAL_LABEL_FILES)
