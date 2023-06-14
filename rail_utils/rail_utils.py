import logging
import random
import time

import cv2
import numpy as np
import pyautogui
import winsound
from PIL import Image

RETRIES_TO_LOAD = 5

logging.basicConfig(level=logging.INFO)


def close_all_pop_ups():
    on_screen, position = image_on_screen(GENERAL_BTN_X_CLOSE)
    while on_screen:
        find_image_and_click([GENERAL_BTN_X_CLOSE], msg="close pop-up")
        sleep_random(1)
        move_mouse_close_to_center()
        sleep_random(1)
        on_screen, position = image_on_screen(GENERAL_BTN_X_CLOSE)


def find_image_and_click(filepaths, msg=None, precision=0.95, screenshot=None, gray_scale=True):
    for _ in range(RETRIES_TO_LOAD):
        wait_rail_response()
        for filepath in filepaths:
            on_screen, position = image_on_screen(filepath, precision=precision, screenshot=screenshot,
                                                  gray_scale=gray_scale)
            if on_screen:
                if msg:
                    logging.info(f"Select: {msg}")
                click_on_rect_area(top_left_corner=position, filepath=filepath)
                return
    if msg:
        raise ImageNotFoundException(f"Fail select: {msg}")
    else:
        raise ImageNotFoundException("Failed to select the image.")


def sleep_random(sleep_time):
    time.sleep(random.uniform(sleep_time, sleep_time * 1.5))


def wait_rail_response():
    sleep_duration = random.uniform(2, 5)
    time.sleep(sleep_duration)


def move_mouse_close_to_center():
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    almost_center_x = random.uniform(center_x - 100, center_x + 100)
    almost_center_y = random.uniform(center_y - 100, center_y + 100)
    pyautogui.moveTo(almost_center_x, almost_center_y)


def click_on_rect_area(top_left_corner, size=None, filepath=None):
    if size is None and filepath is None:
        raise ValueError("Cannot use size and filepath as None at the same time")

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


def image_on_screen(img_str, precision=0.8, screenshot=None, gray_scale=True):
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    img_rgb = np.array(screenshot)

    # Check if we need to convert image to grayscale
    if gray_scale:
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(img_str, 0)
    else:
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
        logging.debug(f"Screenshot captured and saved as {filename}.")
    return screenshot


def beep():
    frequency = 1000
    duration = 200
    winsound.Beep(frequency, duration)


class ImageNotFoundException(Exception):
    pass
