import logging
import unittest

import pyautogui

from invest.industry_invest.industry_invest import RANKING_SHOW_MORE
from rail_utils.rail_utils import get_screenshot, image_on_screen

logging.root.setLevel(logging.DEBUG)


class IsImageOnScreen(unittest.TestCase):
    def test_test_image(self):
        file_path = RANKING_SHOW_MORE
        screenshot = get_screenshot()
        screenshot.save("data/screenshot.png")
        precision = 0.1
        is_on_screen, position = image_on_screen(file_path, precision=precision, screenshot=screenshot, gray_scale=True)
        x, y = position
        pyautogui.moveTo(x=x, y=y)

        self.assertTrue(is_on_screen)


if __name__ == '__main__':
    unittest.main()
