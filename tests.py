import logging
import unittest

import pyautogui

from association.worker_bid.worker_bid import WorkerBid, ASSOCIATION_BID_DISABLED_FILES
from rail_utils.rail_utils import get_screenshot, count_down, any_image_on_screen, image_on_screen
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


def try_get_image_folder(paths_array: list[str], precision=0.1, gray_scale=True):
    count_down()
    screenshot = get_screenshot()
    screenshot.save("data/screenshot.png")
    is_ok, position, _, _ = any_image_on_screen(paths_array,
                                                precision=precision,
                                                screenshot=screenshot,
                                                gray_scale=gray_scale)
    x, y = position
    pyautogui.moveTo(x=x, y=y)
    return is_ok


def try_get_image(image_path: str, precision=0.1, gray_scale=True):
    count_down()
    screenshot = get_screenshot()
    screenshot.save("data/screenshot.png")
    is_ok, position, _ = image_on_screen(image_path,
                                         precision=precision,
                                         screenshot=screenshot,
                                         gray_scale=gray_scale)
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


class MainTest(unittest.TestCase):
    def test(self):
        png_path = "data/tabs_status/engine_selected_small.png"
        self.assertTrue(try_get_image(png_path, gray_scale=True))


if __name__ == '__main__':
    unittest.main()
