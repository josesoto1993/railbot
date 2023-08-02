import logging
import unittest

import pyautogui

from association.worker_bid.worker_bid import WorkerBid
from engines.pax_schedule.pax_schedule import POPUP_TIMETABLE_BASE_SMALL
from rail_utils.rail_utils import get_screenshot, image_on_screen, count_down
from rail_utils.tabs_enum import Tab
from rail_utils.tabs_util import open_tab

logging.root.setLevel(logging.DEBUG)


def try_get_bid_amount():
    count_down()
    wb = WorkerBid()
    bid_amount = wb._get_bid_amount()
    logging.info(f"bid amount: {bid_amount}")
    is_ok = bid_amount > 0
    return is_ok


def try_get_image(file_path: str):
    count_down()
    screenshot = get_screenshot()
    screenshot.save("data/screenshot.png")
    precision = 0.1
    is_ok, position, _ = image_on_screen(file_path,
                                         precision=precision,
                                         screenshot=screenshot,
                                         gray_scale=True)
    x, y = position
    pyautogui.moveTo(x=x, y=y)
    return is_ok


def try_open_tab(tab_enum: Tab):
    try:
        open_tab(tab_enum)
        return True
    except Exception as exception:
        logging.error(str(exception))
        return False


class IsImageOnScreen(unittest.TestCase):
    def test(self):
        self.assertTrue(try_get_image(POPUP_TIMETABLE_BASE_SMALL))


if __name__ == '__main__':
    unittest.main()
