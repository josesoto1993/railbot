import logging
import unittest

from rail_utils.rail_utils import get_screenshot, image_on_screen

logging.basicConfig(level=logging.DEBUG)


class IsImageOnScreen(unittest.TestCase):
    def test_test_image(self):
        file_path = 'data/tabs_status/ranking_on_load.png'
        screenshot = get_screenshot()
        precision = 0.9
        is_on_screen, position = image_on_screen(file_path, precision=precision, screenshot=screenshot)

        self.assertTrue(is_on_screen)


if __name__ == '__main__':
    unittest.main()
