import datetime
import logging
import random

import pyautogui
from PIL import Image

from association.worker_bid.workers import get_worker_data
from rail_utils.folders_paths import ASSOCIATION_FOLDER
from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import image_on_screen, get_image_size, get_screenshot_with_black_out_of_box, \
    find_image_and_click, sleep_random, click_on_rect_area, ImageNotFoundException, any_image_on_screen, \
    get_image_paths_from_folder, timestamped_filename, save_screenshot, ERROR_FOLDER, get_screenshot
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVESTMENT_TARGET_RDM_PX = 5
WORKER_BID_MINUTES_TO_RECHECK = 15
WORKER_BID_MINUTE_FINISH = 55

logging.basicConfig(level=logging.INFO)


def have_bid() -> bool:
    user_label_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/user_label")
    on_screen, _, _, _ = any_image_on_screen(user_label_files)
    return on_screen


def get_worker_info_screenshot() -> Image:
    # Find positions of the images
    bids_by_your_association_label_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/bids_by_aso")
    current_worker_label_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/current_worker")
    highest_bid_label_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/highest_bid")
    on_screen_worker, position_worker, _, _ = any_image_on_screen(current_worker_label_files)
    on_screen_association, position_association, _, _ = any_image_on_screen(bids_by_your_association_label_files)
    on_screen_bid, position_bid, _, _ = any_image_on_screen(highest_bid_label_files)

    # Raise exception if any of the images is not found
    if not (on_screen_worker and on_screen_association and on_screen_bid):
        get_screenshot(save=True, filename=f"{ERROR_FOLDER}/worker_not_found")
        logging.error(f"get_worker_info_screenshot error: {on_screen_worker}/{on_screen_association}/{on_screen_bid}")
        raise ImageNotFoundException("Failed to find one or more required images on screen for worker info")

    # Define the size and the top-left corner of the screenshot box
    top_left_corner = position_worker
    size = (position_association[0] - position_worker[0], position_bid[1] - position_worker[1])

    # Get the screenshot
    return get_screenshot_with_black_out_of_box(top_left_corner, size)


def get_bid_left_corner():
    worker_bid_less_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/worker_bid_less")
    on_screen, position, _, image_path = any_image_on_screen(worker_bid_less_files)

    if on_screen:
        return position, image_path

    get_screenshot(save=True, filename=f"{ERROR_FOLDER}/bid_left_corner_not_found")
    raise ImageNotFoundException("Cant find left corner of bid")


def get_bid_right_corner():
    worker_bid_more_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/worker_bid_more")
    on_screen, position, _, image_path = any_image_on_screen(worker_bid_more_files)

    if on_screen:
        return position, image_path

    get_screenshot(save=True, filename=f"{ERROR_FOLDER}/bid_right_corner_not_found")
    raise ImageNotFoundException("Cant find right corner of bid")


def click_amount_input():
    left_corner, image_path_left_corner = get_bid_left_corner()
    right_corner, _ = get_bid_right_corner()

    _, height = get_image_size(image_path_left_corner)

    target_x = (left_corner[0] + right_corner[0]) / 2
    target_y = left_corner[1] + height / 2
    target = target_x, target_y

    size = INVESTMENT_TARGET_RDM_PX, INVESTMENT_TARGET_RDM_PX

    click_on_rect_area(target, size=size)


def get_target_datetime_if_skip_till_next_worker(current_datetime: datetime) -> datetime:
    # Set next run time to the next hour with adjusted minutes
    target_hour = (current_datetime.hour + 1) % 24
    time_gap = round(random.uniform(WORKER_BID_MINUTES_TO_RECHECK * 2, WORKER_BID_MINUTES_TO_RECHECK * 3) // 4)
    target_minute = WORKER_BID_MINUTE_FINISH - time_gap
    target_datetime = current_datetime.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    # If the target time is in the past, add 1 day
    if target_datetime < current_datetime:
        target_datetime += datetime.timedelta(days=1)

    return target_datetime


class WorkerBid(RailRunnable):
    def __init__(self):
        super().__init__()
        self.task_name = self.__class__.__name__
        self.sleep_is_bid_disabled = 5
        self.sleep_select_worker_details = 5
        self.sleep_click_send_bid = 10
        self.sleep_character_input = 0.5
        self.worker_data = get_worker_data()
        self.skip_till_next_worker = False

    def _run(self):
        self._run_worker_bid()

    def _update_next_run_time(self):
        self.next_run_time = self._get_target_datetime()
        logging.debug(f"Next {self.__class__.__name__} check at {self.next_run_time.time()}")

    def _get_target_datetime(self) -> datetime:
        current_datetime = datetime.datetime.now()
        if self.skip_till_next_worker:
            return get_target_datetime_if_skip_till_next_worker(current_datetime)
        else:
            return current_datetime + datetime.timedelta(minutes=WORKER_BID_MINUTES_TO_RECHECK)

    def _run_worker_bid(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.ASSOCIATION.value)
        if self._is_bid_disabled():
            logging.debug("Cant bid as is disabled")
            self.skip_till_next_worker = False
            return
        self._select_worker_details()
        if have_bid():
            logging.debug("Already bid")
            self.skip_till_next_worker = True
            return
        bid_amount = self._get_bid_amount()
        if bid_amount == 0:
            logging.debug("Not interested in this worker")
            self.skip_till_next_worker = True
            return
        self._do_bid(bid_amount)
        self.skip_till_next_worker = True

    def _is_bid_disabled(self) -> bool:
        sleep_random(self.sleep_is_bid_disabled)
        association_bid_disabled_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/bid_disabled")
        no_room_for_worker_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/no_room_for_worker")
        no_worker_available_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/no_worker_available")

        on_screen_disabled, _, _, _ = any_image_on_screen(association_bid_disabled_files,
                                                          gray_scale=False,
                                                          precision=0.95)
        on_screen_no_room, _, _, _ = any_image_on_screen(no_room_for_worker_files)
        on_screen_no_worker, _, _, _ = any_image_on_screen(no_worker_available_files)

        return on_screen_disabled or on_screen_no_room or on_screen_no_worker

    def _select_worker_details(self):
        worker_label_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/worker_label")
        _, position, _, image_path = any_image_on_screen(worker_label_files)
        _, image_height = get_image_size(image_path)

        size = (pyautogui.size()[0], image_height)

        screenshot = get_screenshot_with_black_out_of_box(position, size)

        worker_details_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/worker_details")
        find_image_and_click(worker_details_files,
                             msg="worker details",
                             screenshot=screenshot,
                             error_filename="fail_select_worker_details")
        sleep_random(self.sleep_select_worker_details)

    def _get_bid_amount(self) -> int:
        screenshot = get_worker_info_screenshot()
        for img_path, amount in self.worker_data:
            on_screen, _, _ = image_on_screen(img_path, screenshot=screenshot)
            if on_screen:
                return amount

        filename = timestamped_filename(filename=ERROR_FOLDER + "/error_worker_not_exist")
        save_screenshot(screenshot=screenshot, filename=filename)
        return 0

    def _do_bid(self, bid_amount: int):
        click_amount_input()
        self._delete_actual_value()
        self._type_bid_amount(bid_amount)
        self._click_send_bid()

    def _delete_actual_value(self):
        for _ in range(10):
            pyautogui.press('backspace')
            sleep_random(self.sleep_character_input)

    def _type_bid_amount(self, bid_amount: int):
        for char in str(bid_amount):
            pyautogui.typewrite(char)
            sleep_random(self.sleep_character_input)

    def _click_send_bid(self):
        sleep_random(self.sleep_click_send_bid)
        send_bid_files = get_image_paths_from_folder(ASSOCIATION_FOLDER + "/send_bid")

        find_image_and_click(send_bid_files,
                             msg="bid send btn",
                             error_filename="fail_click_send_bid",
                             gray_scale=False,
                             precision=0.95)
        sleep_random(self.sleep_click_send_bid)
