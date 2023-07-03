import datetime
import logging
import random
import time

import cv2
import numpy as np
import pyautogui
import winsound
from PIL import Image

DATA_FOLDER = "data/"

BASE_SCREENSHOT_NAME = 'screenshot.png'

RETRIES_TO_LOAD = 5

GENERAL_FOLDER = "data/general"
BTN_X_CLOSE_MAIN = GENERAL_FOLDER + "/btn_x_close_main.png"
BTN_X_CLOSE_MAIN_SMALL = GENERAL_FOLDER + "/btn_x_close_main_small.png"
BTN_X_CLOSE_ALTER = GENERAL_FOLDER + "/btn_x_close_alter.png"
BTN_X_CLOSE_ALTER_SMALL = GENERAL_FOLDER + "/btn_x_close_alter_small.png"
BTN_X_CLOSE = [BTN_X_CLOSE_MAIN,
               BTN_X_CLOSE_MAIN_SMALL,
               BTN_X_CLOSE_ALTER,
               BTN_X_CLOSE_ALTER_SMALL]
BTN_X_TICKET_BASE = GENERAL_FOLDER + "/close_redeem_ticket.png"
BTN_X_TICKET_BASE_SMALL = GENERAL_FOLDER + "/close_redeem_ticket_small.png"
BTN_CONTINUE_BASE = GENERAL_FOLDER + "/continue_playing.png"
BTN_CONTINUE_BASE_SMALL = GENERAL_FOLDER + "/continue_playing_small.png"
ALL_CLOSE_BTN = [BTN_X_CLOSE_MAIN,
                 BTN_X_CLOSE_MAIN_SMALL,
                 BTN_X_CLOSE_ALTER,
                 BTN_X_CLOSE_ALTER_SMALL,
                 BTN_X_TICKET_BASE,
                 BTN_X_TICKET_BASE_SMALL,
                 BTN_CONTINUE_BASE,
                 BTN_CONTINUE_BASE_SMALL]

logging.basicConfig(level=logging.INFO)


def close_all_pop_ups():
    precision = 0.9
    on_screen, _, _, _ = any_image_on_screen(ALL_CLOSE_BTN, precision=precision)
    while on_screen:
        find_image_and_click(ALL_CLOSE_BTN, msg="close pop-up", retries=1, precision=precision)
        sleep_random(1)
        move_mouse_close_to_center()
        sleep_random(1)
        on_screen, _, _, _ = any_image_on_screen(ALL_CLOSE_BTN, precision=precision)


def find_image_and_click(
        filepaths: list[str],
        msg=None,
        precision=0.95,
        screenshot=None,
        gray_scale=True,
        retries=RETRIES_TO_LOAD
):
    for _ in range(retries):
        wait_rail_response()
        for filepath in filepaths:
            on_screen, position, _ = image_on_screen(filepath,
                                                     precision=precision,
                                                     screenshot=screenshot,
                                                     gray_scale=gray_scale)
            if on_screen:
                if msg:
                    logging.debug(f"Select: {msg}")
                click_on_rect_area(top_left_corner=position, filepath=filepath)
                return
    _find_image_and_click_log_error(filepaths, msg)


def _find_image_and_click_log_error(filepaths, msg):
    filename = timestamped_filename(filename="errors/error_find_and_click")
    get_screenshot(save=True, filename=filename)
    msg = msg or "the image"
    raise ImageNotFoundException(f"Fail select: {msg}, for images {filepaths}")


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


def move_mouse_close_to_top_right():
    screen_width, _ = pyautogui.size()
    offset = 10
    pyautogui.moveTo(screen_width - offset, offset)


def click_on_rect_area(top_left_corner, size=None, filepath=None):
    if size is None and filepath is None:
        raise ValueError("Cannot use size and filepath as None at the same time")

    x, y = top_left_corner

    width = 0
    height = 0

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


def get_image_size(image_path: str):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height


def any_image_on_screen(paths_array: list[str], precision=0.8, screenshot=None, gray_scale=True):
    best_max_val = None
    best_max_loc = None
    best_image = None
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    for img_str in paths_array:
        on_screen, max_loc, max_val = image_on_screen(img_str,
                                                      precision=precision,
                                                      screenshot=screenshot,
                                                      gray_scale=gray_scale)

        if on_screen and (best_max_val is None or max_val > best_max_val):
            best_max_val = max_val
            best_max_loc = max_loc
            best_image = img_str

    if best_image is None:
        return False, None, None, None
    else:
        return True, best_max_loc, best_max_val, best_image


def image_on_screen(img_str: str, precision=0.8, screenshot=None, gray_scale=True):
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
        return False, None, max_val
    else:
        return True, max_loc, max_val


def get_screenshot(save=False, filename=BASE_SCREENSHOT_NAME):
    if '.' not in filename:
        filename += '.png'
    screenshot = pyautogui.screenshot()
    if save:
        screenshot.save(DATA_FOLDER + filename)
        logging.debug(f"Screenshot captured and saved as {filename}.")
    return screenshot


def get_screenshot_with_black_box_in(top_left_corner, size, screenshot=None, save=False, filename=BASE_SCREENSHOT_NAME):
    if '.' not in filename:
        filename += '.png'
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    # Get the width and height of the image
    width, height = screenshot.size

    # Use the `load` method to get the pixel data
    pixels = screenshot.load()

    # Define the box coordinates
    box_x_start, box_y_start = top_left_corner
    box_width, box_height = size
    box_x_end = box_x_start + box_width
    box_y_end = box_y_start + box_height

    # Loop over all pixels in the image
    for y in range(height):
        for x in range(width):
            # If the pixel is inside the box, set it to black
            if box_x_start <= x <= box_x_end and box_y_start <= y <= box_y_end:
                pixels[x, y] = (0, 0, 0)

    if save:
        screenshot.save(DATA_FOLDER + filename)
        logging.debug(f"Screenshot captured and saved as {filename}.")

    return screenshot


def get_screenshot_with_black_out_of_box(top_left_corner, size, screenshot=None, save=False,
                                         filename=BASE_SCREENSHOT_NAME):
    if '.' not in filename:
        filename += '.png'
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    # Get the width and height of the image
    width, height = screenshot.size

    # Use the `load` method to get the pixel data
    pixels = screenshot.load()

    # Define the box coordinates
    box_x_start, box_y_start = top_left_corner
    box_width, box_height = size
    box_x_end = box_x_start + box_width
    box_y_end = box_y_start + box_height

    # Loop over all pixels in the image
    for y in range(height):
        for x in range(width):
            # If the pixel is outside the box, set it to black
            if x < box_x_start or box_x_end < x or y < box_y_start or box_y_end < y:
                pixels[x, y] = (0, 0, 0)

    if save:
        screenshot.save(DATA_FOLDER + filename)
        logging.debug(f"Screenshot captured and saved as {filename}.")
    return screenshot


def beep():
    frequency = 1000
    duration = 200
    winsound.Beep(frequency, duration)


def timestamped_filename(filename=""):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d_%H%M%S")
    return f"{filename}_{formatted_time}"


class ImageNotFoundException(Exception):
    pass
