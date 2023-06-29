import logging
import unittest
from time import sleep

import pyautogui

from association.worker_bid.worker_bid import WorkerBid
from association.worker_bid.workers import WORKER_ACCELERATION
from rail_utils.rail_utils import get_screenshot, image_on_screen, beep

logging.root.setLevel(logging.DEBUG)


def count_down():
    sleep(1)
    beep()
    sleep(1)
    beep()
    sleep(1)
    beep()


class IsImageOnScreen(unittest.TestCase):
    def test_test_image(self):
        count_down()

        file_path = WORKER_ACCELERATION
        screenshot = get_screenshot()
        screenshot.save("data/screenshot.png")
        precision = 0.1
        is_on_screen, position, _ = image_on_screen(file_path,
                                                    precision=precision,
                                                    screenshot=screenshot,
                                                    gray_scale=True)
        x, y = position
        pyautogui.moveTo(x=x, y=y)

        self.assertTrue(is_on_screen)

    def test_get_bid_amount(self):
        count_down()

        wb = WorkerBid()
        bid_amount = wb._get_bid_amount()
        logging.info(f"bid amount: {bid_amount}")

        self.assertTrue(bid_amount > 0)


if __name__ == '__main__':
    unittest.main()
