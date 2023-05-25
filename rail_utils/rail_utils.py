import logging
import random
import time

import cv2
import numpy as np
import pyautogui
from PIL import Image

RETRIES_TO_LOAD = 5

logging.basicConfig(level=logging.INFO)


def find_image_and_click(filepaths, on_screen_msg=None, on_fail_msg=None, precision=0.95):
    for _ in range(RETRIES_TO_LOAD):
        wait_rail_response()
        for filepath in filepaths:
            on_screen, position = image_on_screen(filepath, precision=precision)
            if on_screen:
                if on_screen_msg:
                    logging.info(on_screen_msg)
                click_on_rect_area(top_left_corner=position, filepath=filepath)
                return
    raise Exception(on_fail_msg)


def wait_rail_response():
    sleep_duration = random.uniform(2, 5)
    time.sleep(sleep_duration)


def move_mouse_to_center():
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.moveTo(center_x, center_y)


def click_on_rect_area(top_left_corner, size=None, filepath=None):
    if size is None and filepath is None:
        raise Exception("Cannot use size and filepath as None at the same time")

    x, y = top_left_corner

    if size:
        width, height = size

    if filepath:
        width, height = get_image_size(filepath)

    # Calculate the random position within the rectangle
    random_x = x + random.uniform(0, width)
    random_y = y + random.uniform(0, height)

    # Move the mouse to the random position and click
    pyautogui.moveTo(random_x, random_y)
    pyautogui.click()


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height


def image_on_screen(img_str, precision=0.8, screenshot=None):
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    img_rgb = np.array(screenshot)
    template = cv2.imread(img_str)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    logging.debug(f"path: {img_str}, max_val: {max_val}")

    if max_val < precision:
        return False, None
    else:
        return True, max_loc


def get_screenshot(save=False, filename='screenshot.png'):
    if '.' not in filename:
        filename += '.png'
    screenshot = pyautogui.screenshot()
    if save:
        screenshot.save("data/" + filename)
        print(f"Screenshot captured and saved as {filename}.")
    return screenshot


import winsound


def beep():
    frequency = 1000
    duration = 200
    winsound.Beep(frequency, duration)
