import datetime
import logging
import os
import random
import time
from typing import Tuple, Optional

import cv2
import numpy as np
import pyautogui
import winsound
from PIL import Image

from rail_utils.folders_paths import ERROR_FOLDER, DATA_FOLDER, INTERRUPT_FOLDER, CONTINUE_FOLDER, BTN_X_FOLDER

BASE_SCREENSHOT_NAME = 'screenshot.png'

RETRIES_TO_LOAD = 5
MAX_CLOSE_RETRIES = 20

logging.basicConfig(level=logging.INFO)


def close_all_pop_ups():
    logging.debug("close all pop ups")
    pop_up_close_img_paths = (
            get_image_paths_from_folder(BTN_X_FOLDER) +
            get_image_paths_from_folder(CONTINUE_FOLDER) +
            get_image_paths_from_folder(INTERRUPT_FOLDER)
    )

    max_retries = MAX_CLOSE_RETRIES
    retries = 0

    while retries < max_retries:
        on_screen, _, _, _ = any_image_on_screen(pop_up_close_img_paths)
        logging.debug(f"any to close? {on_screen}")

        if not on_screen:
            break

        find_image_and_click(pop_up_close_img_paths,
                             msg="close pop-up",
                             retries=1,
                             error_filename="fail_close_all_pop_ups")
        sleep_random(1)
        move_mouse_close_to_top_right()
        sleep_random(1)

        retries += 1

    if retries == max_retries:
        get_screenshot(save=True, filename=f"{ERROR_FOLDER}/error_close_popup_max_retries")
        raise MaxClosePopUpRetriesExceededError("Exceeded maximum retries for closing pop-ups.")


def find_image_and_click(
        filepaths: list[str],
        msg=None,
        precision=0.8,
        screenshot=None,
        gray_scale=True,
        retries=RETRIES_TO_LOAD,
        error_filename=None
):
    for _ in range(retries):
        wait_rail_response()
        on_screen, position, _, best_match_filepath = any_image_on_screen(
            filepaths,
            precision=precision,
            screenshot=screenshot,
            gray_scale=gray_scale
        )

        if on_screen:
            if msg:
                logging.debug(f"Select: {msg} - best image is: {best_match_filepath}")
            click_on_rect_area(top_left_corner=position, filepath=best_match_filepath)
            return

    _find_image_and_click_log_error(filepaths, msg=msg, filename=error_filename, screenshot=screenshot)


def _find_image_and_click_log_error(filepaths, msg, filename=None, screenshot=None):
    if filename is None:
        filename = timestamped_filename(filename=f"{ERROR_FOLDER}/error_find_and_click")
    else:
        filename = ERROR_FOLDER + "/" + filename

    if screenshot is None:
        get_screenshot(save=True, filename=filename)
    else:
        save_screenshot(filename=filename, screenshot=screenshot)

    msg = msg or "the image"
    raise ImageNotFoundException(f"Fail select: {msg}, for images {filepaths}")


def sleep_random(sleep_time):
    sleep_duration = random.uniform(sleep_time, sleep_time * 1.5)
    logging.debug(f"sleep for: {sleep_duration} sec")
    time.sleep(sleep_duration)


def wait_rail_response():
    sleep_duration = random.uniform(2, 5)
    logging.debug(f"sleep for: {sleep_duration} sec")
    time.sleep(sleep_duration)


def move_mouse_close_to_center():
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    almost_center_x = random.uniform(center_x - 100, center_x + 100)
    almost_center_y = random.uniform(center_y - 100, center_y + 100)
    pyautogui.moveTo(almost_center_x, almost_center_y)


def move_mouse_close_to_top_right():
    logging.debug("move_mouse_close_to_top_right")
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


def get_image_size(image_path: str) -> Tuple[int, int]:
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height


def any_image_on_screen(paths_array: list[str],
                        precision=0.8,
                        screenshot=None,
                        gray_scale=True) -> Tuple[bool, Optional[Tuple[int, int]], Optional[float], Optional[str]]:
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


def image_on_screen(img_str: str,
                    precision=0.8,
                    screenshot: Image = None,
                    gray_scale=True) -> Tuple[bool, Optional[Tuple[int, int]], Optional[float]]:
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


def get_screenshot(save=False, filename=BASE_SCREENSHOT_NAME) -> Image:
    logging.debug("get_screenshot")
    screenshot = pyautogui.screenshot()
    if save:
        save_screenshot(filename, screenshot)
    return screenshot


def save_screenshot(filename, screenshot):
    if '.' not in filename:
        filename += '.png'
    screenshot.save(DATA_FOLDER + filename)
    logging.debug(f"Screenshot captured and saved as {filename}.")


def get_image_paths_from_folder(folder: str) -> list[str]:
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(folder)
        for file in files
        if file.lower().endswith('.png')
    ]


def get_folder_paths_from_folder(folder: str) -> list[str]:
    return [
        os.path.join(root, subfolder)
        for root, subfolders, _ in os.walk(folder)
        for subfolder in subfolders
    ]


def get_screenshot_with_black_box_in(top_left_corner,
                                     size,
                                     screenshot=None,
                                     save=False,
                                     filename=BASE_SCREENSHOT_NAME) -> Image:
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


def get_screenshot_with_black_out_of_box(top_left_corner,
                                         size,
                                         screenshot=None,
                                         save=False,
                                         filename=BASE_SCREENSHOT_NAME) -> Image:
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


def count_down(sleep_time=1, count=3):
    for _ in range(count):
        time.sleep(sleep_time)
        beep()


def timestamped_filename(filename="") -> str:
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d_%H%M%S")
    return f"{filename}_{formatted_time}"


class ImageNotFoundException(Exception):
    pass


class MaxClosePopUpRetriesExceededError(Exception):
    pass
