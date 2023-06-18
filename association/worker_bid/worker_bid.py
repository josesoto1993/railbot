import datetime
import logging

import pyautogui

from rail_utils.rail_utils import image_on_screen, get_image_size, get_screenshot_with_black_out_of_box, \
    find_image_and_click, sleep_random, click_on_rect_area
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVESTMENT_TARGET_RDM_PX = 5
WORKER_BID_MINUTES_TO_RECHECK = 45
ASSOCIATION_BID_DISABLED = "data/tab_association/bid_disabled.png"
ASSOCIATION_NO_ROOM_FOR_WORKER = "data/tab_association/no_room_for_worker.png"
ASSOCIATION_NO_WORKER_AVAILABLE = "data/tab_association/no_worker_available.png"
ASSOCIATION_WORKER_LABEL = "data/tab_association/worker_label.png"
ASSOCIATION_WORKER_DETAILS = "data/tab_association/worker_details_btn.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL = "data/tab_association/user_bid_label.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER = "data/tab_association/user_bid_label_hover.png"
ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED = "data/tab_association/minus_bid_btn_enabled.png"
ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED = "data/tab_association/minus_bid_btn_disabled.png"
ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED = "data/tab_association/plus_bid_btn_enabled.png"
ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED = "data/tab_association/plus_bid_btn_disabled.png"
ASSOCIATION_WORKER_DETAILS_SEND_BID_BTN = "data/tab_association/send_bid_btn.png"


def have_bid():
    on_screen, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_USER_LABEL)
    on_screen_hover, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER)

    return on_screen or on_screen_hover


def get_investment_amount():
    # TODO: create a real function
    return 77777


def get_bid_left_corner():
    on_screen_enabled, left_corner_enabled = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED)
    if on_screen_enabled:
        return left_corner_enabled
    on_screen_disabled, left_corner_disabled = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED)
    if on_screen_disabled:
        return left_corner_disabled
    raise Exception(f"Cant find left corner of bid")


def get_bid_right_corner():
    on_screen_enabled, right_corner_enabled = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED)
    if on_screen_enabled:
        return right_corner_enabled
    on_screen_disabled, right_corner_disabled = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED)
    if on_screen_disabled:
        return right_corner_disabled
    raise Exception(f"Cant find right corner of bid")


def click_amount_input():
    left_corner = get_bid_left_corner()
    right_corner = get_bid_right_corner()

    _, height = get_image_size(ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED)

    target_x = (left_corner[0] + right_corner[0]) / 2
    target_y = left_corner[1] + height / 2
    target = target_x, target_y

    size = INVESTMENT_TARGET_RDM_PX, INVESTMENT_TARGET_RDM_PX

    click_on_rect_area(target, size=size)


class WorkerBid:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_is_bid_disabled = 5
        self.sleep_select_worker_details = 5
        self.sleep_bid_worker = 10
        self.sleep_set_investment_amount = 5
        self.sleep_send_bid = 10
        self.sleep_delete_one_character = 0.5

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
        if self._is_bid_disabled():
            logging.info(f"Cant bid as is disabled")
            return
        self._select_worker_details()
        if have_bid():
            logging.info(f"Already bid")
            return
        investment_amount = get_investment_amount()
        if investment_amount == 0:
            logging.info(f"Not interested in this worker")
            return
        self._set_investment_amount(investment_amount)
        self._send_bid()

    def _is_bid_disabled(self):
        sleep_random(self.sleep_is_bid_disabled)
        on_screen_disabled, _ = image_on_screen(ASSOCIATION_BID_DISABLED, gray_scale=False)
        on_screen_no_room, _ = image_on_screen(ASSOCIATION_NO_ROOM_FOR_WORKER)
        on_screen_no_worker, _ = image_on_screen(ASSOCIATION_NO_WORKER_AVAILABLE)

        return on_screen_disabled or on_screen_no_room or on_screen_no_worker

    def _select_worker_details(self):
        on_screen, position = image_on_screen(ASSOCIATION_WORKER_LABEL)
        image_width, image_height = get_image_size(ASSOCIATION_WORKER_LABEL)

        size = (pyautogui.size()[0], image_height)

        screenshot = get_screenshot_with_black_out_of_box(position, size)

        find_image_and_click([ASSOCIATION_WORKER_DETAILS], msg="select worker details", screenshot=screenshot)
        sleep_random(self.sleep_select_worker_details)

    def _set_investment_amount(self, investment_amount):
        click_amount_input()
        self._delete_actual_value()

        sleep_random(self.sleep_set_investment_amount)
        raise Exception(f"Implement: _set_investment_amount")

    def _delete_actual_value(self):
        for _ in range(10):
            pyautogui.press('backspace')
            sleep_random(self.sleep_delete_one_character)

    def _send_bid(self):
        sleep_random(self.sleep_send_bid)
        raise Exception(f"Implement: _send_bid")

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=WORKER_BID_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next worker bid check at {target_datetime.time()} -----")
