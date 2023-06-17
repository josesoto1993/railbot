import datetime
import logging

import pyautogui

from rail_utils.rail_utils import image_on_screen, get_image_size, get_screenshot_with_black_out_of_box, \
    find_image_and_click, sleep_random
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

WORKER_BID_MINUTES_TO_RECHECK = 45
ASSOCIATION_BID_DISABLED = "data/tab_association/bid_disabled.png"
ASSOCIATION_NO_ROOM_FOR_WORKER = "data/tab_association/no_room_for_worker.png"
ASSOCIATION_NO_WORKER_AVAILABLE = "data/tab_association/no_worker_available.png"
ASSOCIATION_WORKER_LABEL = "data/tab_association/worker_label.png"
ASSOCIATION_WORKER_DETAILS = "data/tab_association/worker_details_btn.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL = "data/tab_association/user_bid_label.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER = "data/tab_association/user_bid_label_hover.png"


def is_bid_disabled():
    on_screen_disabled, _ = image_on_screen(ASSOCIATION_BID_DISABLED)
    on_screen_no_room, _ = image_on_screen(ASSOCIATION_NO_ROOM_FOR_WORKER)
    on_screen_no_worker, _ = image_on_screen(ASSOCIATION_NO_WORKER_AVAILABLE)

    return on_screen_disabled or on_screen_no_room or on_screen_no_worker


def have_bid():
    on_screen, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_USER_LABEL)
    on_screen_hover, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER)

    return on_screen or on_screen_hover


class WorkerBid:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_select_worker_details = 5

    def run(self):
        if self._should_run():
            try:
                self._run_worker_bid()
                self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_worker_bid(self):
        logging.info(f"----- Run worker bid: Start at {datetime.datetime.now()} -----")
        open_tab(Tabs.ASSOCIATION)
        if is_bid_disabled():
            logging.info(f"Cant bid as is disabled")
            return
        self._select_worker_details()
        if have_bid():
            logging.info(f"Already bid")
            return
        self._select_bid_on_worker()

    def _select_worker_details(self):
        on_screen, position = image_on_screen(ASSOCIATION_WORKER_LABEL)
        image_width, image_height = get_image_size(ASSOCIATION_WORKER_LABEL)

        size = (pyautogui.size()[0], image_height)

        screenshot = get_screenshot_with_black_out_of_box(position, size)

        find_image_and_click([ASSOCIATION_WORKER_DETAILS], msg="select worker details", screenshot=screenshot)
        sleep_random(self.sleep_select_worker_details)

    def _select_bid_on_worker(self):
        sleep_random(self.sleep_select_worker_details)

        self._update_next_run_time()
        raise Exception(f"Implement: _run_worker_bid")

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=WORKER_BID_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next worker bid check at {target_datetime.time()} -----")
