import datetime
import logging

import pyautogui

from rail_utils.rail_utils import sleep_random, find_image_and_click, move_mouse_close_to_center, image_on_screen, \
    click_on_rect_area, close_all_pop_ups, get_screenshot, ImageNotFoundException, get_image_size

MAX_ZOOM_CLICKS = 10
CITY_HEIGHT = 80
CITY_WIDTH = 120
HEIGHT_OFFSET = 70
INVEST_MINUTES_TO_RECHECK = 180
MAP_BTN_CENTER = "data/map/btn_center.png"
BTN_ZOOM_IN_BASE = "data/map/btn_zoom_in_base.png"
BTN_ZOOM_IN_DISABLED = "data/map/btn_zoom_in_disabled.png"
CITY_SUBTAB_CITY_PROJECT = "data/city/city_subtab_city_project.png"
CITY_LABEL_LEFT = "data/city/city_label_left.png"
CITY_LABEL_RIGHT = "data/city/city_label_right.png"


def get_city_label():
    left_on_screen, left_position = image_on_screen(CITY_LABEL_LEFT)
    right_on_screen, right_position = image_on_screen(CITY_LABEL_RIGHT)

    if not left_on_screen and not right_on_screen:
        raise ImageNotFoundException(f"Fail cet city label.")

    left_width, left_height = get_image_size(CITY_LABEL_LEFT)
    right_width, right_height = get_image_size(CITY_LABEL_RIGHT)

    x_start = left_position[0] + left_width
    y_start = left_position[1]
    x_finish = right_position[0]
    y_finish = right_position[1] + right_height
    boundaries = (x_start, y_start, x_finish, y_finish)

    full_screenshot = get_screenshot()
    city_label = full_screenshot.crop(boundaries)

    return city_label


class CityInvest:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_center_city = 3
        self.sleep_zoom = 2
        self.sleep_select_city = 10
        self.sleep_select_subtab_city_project = 5
        self.sleep_donate_if_needed = 5
        self.sleep_select_next_city = 5

    def run(self):
        if self._should_run():
            try:
                self._run_invest()
                self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_invest(self):
        logging.info(f"----- Run city invest: Start -----")
        self._center_and_zoom_to_city()
        self._select_city()
        self._select_subtab_city_project()
        self._check_all_cities()

    def _center_and_zoom_to_city(self):
        close_all_pop_ups()

        precision = 0.992
        on_screen, position = image_on_screen(BTN_ZOOM_IN_BASE, precision=precision)
        tries = 0
        while on_screen and tries < MAX_ZOOM_CLICKS:
            tries += 1
            find_image_and_click([BTN_ZOOM_IN_BASE], msg="zoom")
            sleep_random(self.sleep_zoom / 2)
            move_mouse_close_to_center()
            sleep_random(self.sleep_zoom / 2)
            on_screen, position = image_on_screen(BTN_ZOOM_IN_BASE, precision=precision)

        find_image_and_click([MAP_BTN_CENTER], msg="center map")
        sleep_random(self.sleep_center_city)

    def _select_city(self):
        screen_width, screen_height = pyautogui.size()
        top_left_corner = ((screen_width - CITY_WIDTH) // 2, (screen_height + HEIGHT_OFFSET - CITY_HEIGHT) // 2)
        size = (CITY_WIDTH, CITY_HEIGHT)
        click_on_rect_area(top_left_corner, size)

        sleep_random(self.sleep_select_city)

    def _select_subtab_city_project(self):
        find_image_and_click([CITY_SUBTAB_CITY_PROJECT], msg="subtab city project")
        sleep_random(self.sleep_select_subtab_city_project)

    def _check_all_cities(self):
        start_city_label = get_city_label()
        start_city_label_filename = 'data/city/start_city_label.png'
        start_city_label.save(start_city_label_filename)
        on_screen = False
        while not on_screen:
            self._donate_if_needed()
            self._select_next_city()
            on_screen, position = image_on_screen(start_city_label_filename)

    def _donate_if_needed(self):
        logging.error("Implement donate_if_needed")
        sleep_random(self.sleep_donate_if_needed)

    def _select_next_city(self):
        find_image_and_click([CITY_LABEL_RIGHT], msg="select next city")
        sleep_random(self.sleep_select_next_city)

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next city invest at {target_datetime.time()} -----")
