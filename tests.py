import logging
import unittest
from time import sleep

import pyautogui

from association.worker_bid.worker_bid import WorkerBid
from rail_utils.rail_utils import get_screenshot, image_on_screen, beep

logging.root.setLevel(logging.DEBUG)


def count_down():
    sleep(1)
    beep()
    sleep(1)
    beep()
    sleep(1)
    beep()


def try_get_bid_amount():
    count_down()
    wb = WorkerBid()
    bid_amount = wb._get_bid_amount()
    logging.info(f"bid amount: {bid_amount}")
    is_ok = bid_amount > 0
    return is_ok


def try_get_image():
    count_down()
    file_path = "data/general/continue_playing_small.png"
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


class IsImageOnScreen(unittest.TestCase):
    def test(self):
        self.assertTrue(try_get_image())


if __name__ == '__main__':
    unittest.main()
