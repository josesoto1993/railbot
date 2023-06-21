import datetime
import logging

import pyautogui

from rail_utils.rail_utils import image_on_screen, get_image_size, get_screenshot_with_black_out_of_box, \
    find_image_and_click, sleep_random, click_on_rect_area, ImageNotFoundException
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVESTMENT_TARGET_RDM_PX = 5
WORKER_BID_MINUTES_TO_RECHECK = 15
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
CURRENT_WORKER_LABEL = "data/tab_association/current_worker_label.png"
BIDS_BY_YOUR_ASSOCIATION_LABEL = "data/tab_association/bids_by_aso_label.png"
HIGHEST_BID_LABEL = "data/tab_association/highest_bid_label.png"

logging.basicConfig(level=logging.INFO)


def have_bid():
    on_screen, _, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_USER_LABEL)
    on_screen_hover, _, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER)

    return on_screen or on_screen_hover


def get_worker_info_screenshot():
    # Find positions of the images
    on_screen_worker, position_worker, _ = image_on_screen(CURRENT_WORKER_LABEL)
    on_screen_association, position_association, _ = image_on_screen(BIDS_BY_YOUR_ASSOCIATION_LABEL)
    on_screen_bid, position_bid, _ = image_on_screen(HIGHEST_BID_LABEL)

    # Raise exception if any of the images is not found
    if not (on_screen_worker and on_screen_association and on_screen_bid):
        raise ImageNotFoundException("Failed to find one or more required images on screen for worker info")

    # Define the size and the top-left corner of the screenshot box
    top_left_corner = position_worker
    size = (position_association[0] - position_worker[0], position_bid[1] - position_worker[1])

    # Get the screenshot
    return get_screenshot_with_black_out_of_box(top_left_corner, size)


def get_bid_left_corner():
    on_screen_enabled, left_corner_enabled, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED)
    if on_screen_enabled:
        return left_corner_enabled
    on_screen_disabled, left_corner_disabled, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED)
    if on_screen_disabled:
        return left_corner_disabled
    raise ImageNotFoundException(f"Cant find left corner of bid")


def get_bid_right_corner():
    on_screen_enabled, right_corner_enabled, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED)
    if on_screen_enabled:
        return right_corner_enabled
    on_screen_disabled, right_corner_disabled, _ = image_on_screen(ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED)
    if on_screen_disabled:
        return right_corner_disabled
    raise ImageNotFoundException(f"Cant find right corner of bid")


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
    def __init__(self, worker_data):
        self.next_run_time = datetime.datetime.now()
        self.sleep_is_bid_disabled = 5
        self.sleep_select_worker_details = 5
        self.sleep_click_send_bid = 10
        self.sleep_character_input = 0.5
        self.worker_data = worker_data

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
        open_tab(Tabs.ASSOCIATION.value)
        if self._is_bid_disabled():
            logging.debug(f"Cant bid as is disabled")
            return
        self._select_worker_details()
        if have_bid():
            logging.debug(f"Already bid")
            return
        bid_amount = self._get_bid_amount()
        if bid_amount == 0:
            logging.debug(f"Not interested in this worker")
            return
        self._do_bid(bid_amount)

    def _is_bid_disabled(self):
        sleep_random(self.sleep_is_bid_disabled)
        on_screen_disabled, _, _ = image_on_screen(ASSOCIATION_BID_DISABLED, gray_scale=False)
        on_screen_no_room, _, _ = image_on_screen(ASSOCIATION_NO_ROOM_FOR_WORKER)
        on_screen_no_worker, _, _ = image_on_screen(ASSOCIATION_NO_WORKER_AVAILABLE)

        return on_screen_disabled or on_screen_no_room or on_screen_no_worker

    def _select_worker_details(self):
        on_screen, position, _ = image_on_screen(ASSOCIATION_WORKER_LABEL)
        image_width, image_height = get_image_size(ASSOCIATION_WORKER_LABEL)

        size = (pyautogui.size()[0], image_height)

        screenshot = get_screenshot_with_black_out_of_box(position, size)

        find_image_and_click([ASSOCIATION_WORKER_DETAILS], msg="worker details", screenshot=screenshot)
        sleep_random(self.sleep_select_worker_details)

    def _get_bid_amount(self):
        screenshot = get_worker_info_screenshot()
        for img_path, amount in self.worker_data:
            on_screen, position, _ = image_on_screen(img_path, screenshot=screenshot, precision=0.7)
            if on_screen:
                return amount

        return 0

    def _do_bid(self, bid_amount):
        click_amount_input()
        self._delete_actual_value()
        self._type_investment_amount(bid_amount)
        self._click_send_bid()

    def _delete_actual_value(self):
        for _ in range(10):
            pyautogui.press('backspace')
            sleep_random(self.sleep_character_input)

    def _type_investment_amount(self, investment_amount):
        for char in str(investment_amount):
            pyautogui.typewrite(char)
            sleep_random(self.sleep_character_input)

    def _click_send_bid(self):
        find_image_and_click([ASSOCIATION_WORKER_DETAILS_SEND_BID_BTN], msg="bid send btn")
        sleep_random(self.sleep_click_send_bid)

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=WORKER_BID_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next worker bid check at {target_datetime.time()} -----")
