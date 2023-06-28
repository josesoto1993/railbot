import datetime
import logging

import pyautogui

from association.worker_bid.worker_price_data import get_worker_data
from rail_utils.rail_utils import image_on_screen, get_image_size, get_screenshot_with_black_out_of_box, \
    find_image_and_click, sleep_random, click_on_rect_area, ImageNotFoundException, any_image_on_screen
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVESTMENT_TARGET_RDM_PX = 5
WORKER_BID_MINUTES_TO_RECHECK = 15
WORKER_BID_MINUTE_FINISH = 55

ASSOCIATION_FOLDER = "data/tab_association"
ASSOCIATION_BID_DISABLED = ASSOCIATION_FOLDER + "/bid_disabled.png"
ASSOCIATION_BID_DISABLED_SMALL = ASSOCIATION_FOLDER + "/bid_disabled_small.png"
ASSOCIATION_NO_ROOM_FOR_WORKER = ASSOCIATION_FOLDER + "/no_room_for_worker.png"
ASSOCIATION_NO_ROOM_FOR_WORKER_SMALL = ASSOCIATION_FOLDER + "/no_room_for_worker_small.png"
ASSOCIATION_NO_WORKER_AVAILABLE = ASSOCIATION_FOLDER + "/no_worker_available.png"
ASSOCIATION_NO_WORKER_AVAILABLE_SMALL = ASSOCIATION_FOLDER + "/no_worker_available_small.png"
ASSOCIATION_WORKER_LABEL = ASSOCIATION_FOLDER + "/worker_label.png"
ASSOCIATION_WORKER_LABEL_SMALL = ASSOCIATION_FOLDER + "/worker_label_small.png"
ASSOCIATION_WORKER_DETAILS = ASSOCIATION_FOLDER + "/worker_details_btn.png"
ASSOCIATION_WORKER_DETAILS_SMALL = ASSOCIATION_FOLDER + "/worker_details_btn_small.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL = ASSOCIATION_FOLDER + "/user_bid_label.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL_SMALL = ASSOCIATION_FOLDER + "/user_bid_label_small.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER = ASSOCIATION_FOLDER + "/user_bid_label_hover.png"
ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER_SMALL = ASSOCIATION_FOLDER + "/user_bid_label_hover_small.png"
ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED = ASSOCIATION_FOLDER + "/minus_bid_btn_enabled.png"
ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED_SMALL = ASSOCIATION_FOLDER + "/minus_bid_btn_enabled_small.png"
ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED = ASSOCIATION_FOLDER + "/minus_bid_btn_disabled.png"
ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED_SMALL = ASSOCIATION_FOLDER + "/minus_bid_btn_disabled_small.png"
ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED = ASSOCIATION_FOLDER + "/plus_bid_btn_enabled.png"
ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED_SMALL = ASSOCIATION_FOLDER + "/plus_bid_btn_enabled_small.png"
ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED = ASSOCIATION_FOLDER + "/plus_bid_btn_disabled.png"
ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED_SMALL = ASSOCIATION_FOLDER + "/plus_bid_btn_disabled_small.png"
ASSOCIATION_WORKER_DETAILS_SEND_BID_BTN = ASSOCIATION_FOLDER + "/send_bid_btn.png"
ASSOCIATION_WORKER_DETAILS_SEND_BID_BTN_SMALL = ASSOCIATION_FOLDER + "/send_bid_btn_small.png"
CURRENT_WORKER_LABEL = ASSOCIATION_FOLDER + "/current_worker_label.png"
CURRENT_WORKER_LABEL_SMALL = ASSOCIATION_FOLDER + "/current_worker_label_small.png"
BIDS_BY_YOUR_ASSOCIATION_LABEL = ASSOCIATION_FOLDER + "/bids_by_aso_label.png"
BIDS_BY_YOUR_ASSOCIATION_LABEL_SMALL = ASSOCIATION_FOLDER + "/bids_by_aso_label_small.png"
HIGHEST_BID_LABEL = ASSOCIATION_FOLDER + "/highest_bid_label.png"
HIGHEST_BID_LABEL_SMALL = ASSOCIATION_FOLDER + "/highest_bid_label_small.png"

logging.basicConfig(level=logging.INFO)


def have_bid():
    on_screen, _, _, _ = any_image_on_screen(
        [ASSOCIATION_WORKER_DETAILS_USER_LABEL,
         ASSOCIATION_WORKER_DETAILS_USER_LABEL_SMALL,
         ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER,
         ASSOCIATION_WORKER_DETAILS_USER_LABEL_HOVER_SMALL])

    return on_screen


def get_worker_info_screenshot():
    # Find positions of the images
    worker_label = [CURRENT_WORKER_LABEL, CURRENT_WORKER_LABEL_SMALL]
    on_screen_worker, position_worker, _, _ = any_image_on_screen(worker_label)
    bids_by_your_association_label = [BIDS_BY_YOUR_ASSOCIATION_LABEL, BIDS_BY_YOUR_ASSOCIATION_LABEL_SMALL]
    on_screen_association, position_association, _, _ = any_image_on_screen(bids_by_your_association_label)
    highest_bid_label = [HIGHEST_BID_LABEL, HIGHEST_BID_LABEL_SMALL]
    on_screen_bid, position_bid, _, _ = any_image_on_screen(highest_bid_label)

    # Raise exception if any of the images is not found
    if not (on_screen_worker and on_screen_association and on_screen_bid):
        raise ImageNotFoundException("Failed to find one or more required images on screen for worker info")

    # Define the size and the top-left corner of the screenshot box
    top_left_corner = position_worker
    size = (position_association[0] - position_worker[0], position_bid[1] - position_worker[1])

    # Get the screenshot
    return get_screenshot_with_black_out_of_box(top_left_corner, size)


def get_bid_left_corner():
    worker_details_bid_less = [ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED,
                               ASSOCIATION_WORKER_DETAILS_BID_LESS_ENABLED_SMALL,
                               ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED,
                               ASSOCIATION_WORKER_DETAILS_BID_LESS_DISABLED_SMALL]
    on_screen, position, _, image_path = any_image_on_screen(worker_details_bid_less)
    if on_screen:
        return position, image_path

    raise ImageNotFoundException(f"Cant find left corner of bid")


def get_bid_right_corner():
    worker_details_bid_more = [ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED,
                               ASSOCIATION_WORKER_DETAILS_BID_MORE_ENABLED_SMALL,
                               ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED,
                               ASSOCIATION_WORKER_DETAILS_BID_MORE_DISABLED_SMALL]
    on_screen, position, _, image_path = image_on_screen(worker_details_bid_more)
    if on_screen:
        return position, image_path

    raise ImageNotFoundException(f"Cant find right corner of bid")


def click_amount_input():
    left_corner, image_path_left_corner = get_bid_left_corner()
    right_corner, _ = get_bid_right_corner()

    _, height = get_image_size(image_path_left_corner)

    target_x = (left_corner[0] + right_corner[0]) / 2
    target_y = left_corner[1] + height / 2
    target = target_x, target_y

    size = INVESTMENT_TARGET_RDM_PX, INVESTMENT_TARGET_RDM_PX

    click_on_rect_area(target, size=size)


def get_target_datetime(bid_done, current_datetime):
    if bid_done:
        target_datetime = get_target_datetime_if_bid(current_datetime)
    else:
        target_datetime = current_datetime + datetime.timedelta(minutes=WORKER_BID_MINUTES_TO_RECHECK)
    return target_datetime


def get_target_datetime_if_bid(current_datetime):
    # Set next run time to the next hour with adjusted minutes
    target_hour = (current_datetime.hour + 1) % 24
    target_minute = WORKER_BID_MINUTE_FINISH - WORKER_BID_MINUTES_TO_RECHECK // 2
    target_datetime = current_datetime.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    # If the target time is in the past, add 1 day
    if target_datetime < current_datetime:
        target_datetime += datetime.timedelta(days=1)

    return target_datetime


class WorkerBid:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_is_bid_disabled = 5
        self.sleep_select_worker_details = 5
        self.sleep_click_send_bid = 10
        self.sleep_character_input = 0.5
        self.worker_data = get_worker_data()

    def run(self):
        if self._should_run():
            try:
                bid_done = self._run_worker_bid()
                self._update_next_run_time(bid_done)
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
            return False
        self._select_worker_details()
        if have_bid():
            logging.debug(f"Already bid")
            return False
        bid_amount = self._get_bid_amount()
        if bid_amount == 0:
            logging.debug(f"Not interested in this worker")
            return False
        self._do_bid(bid_amount)
        return True

    def _is_bid_disabled(self):
        sleep_random(self.sleep_is_bid_disabled)
        bid_disabled = [ASSOCIATION_BID_DISABLED, ASSOCIATION_BID_DISABLED_SMALL]
        on_screen_disabled, _, _, _ = any_image_on_screen(bid_disabled, gray_scale=False)
        no_room_for_worker = [ASSOCIATION_NO_ROOM_FOR_WORKER, ASSOCIATION_NO_ROOM_FOR_WORKER_SMALL]
        on_screen_no_room, _, _, _ = any_image_on_screen(no_room_for_worker)
        no_worker_available = [ASSOCIATION_NO_WORKER_AVAILABLE, ASSOCIATION_NO_WORKER_AVAILABLE_SMALL]
        on_screen_no_worker, _, _, _ = any_image_on_screen(no_worker_available)

        return on_screen_disabled or on_screen_no_room or on_screen_no_worker

    def _select_worker_details(self):
        worker_label = [ASSOCIATION_WORKER_LABEL, ASSOCIATION_WORKER_LABEL_SMALL]
        on_screen, position, _, image_path = any_image_on_screen(worker_label)
        image_width, image_height = get_image_size(image_path)

        size = (pyautogui.size()[0], image_height)

        screenshot = get_screenshot_with_black_out_of_box(position, size)

        worker_details = [ASSOCIATION_WORKER_DETAILS, ASSOCIATION_WORKER_DETAILS_SMALL]
        find_image_and_click(worker_details, msg="worker details", screenshot=screenshot)
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
        worker_details_send_btn = [ASSOCIATION_WORKER_DETAILS_SEND_BID_BTN,
                                   ASSOCIATION_WORKER_DETAILS_SEND_BID_BTN_SMALL]
        find_image_and_click(worker_details_send_btn, msg="bid send btn")
        sleep_random(self.sleep_click_send_bid)

    def _update_next_run_time(self, bid_done=True):
        current_datetime = datetime.datetime.now()
        self.next_run_time = get_target_datetime(bid_done, current_datetime)
        logging.info(f"----- Next worker bid check at {self.next_run_time.time()} -----")
