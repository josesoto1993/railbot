import datetime
import logging

import pyautogui

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import any_image_on_screen, image_on_screen, ImageNotFoundException, get_image_size, \
    get_screenshot, get_screenshot_with_black_out_of_box, close_all_pop_ups, sleep_random, find_image_and_click, \
    move_mouse_close_to_center, click_on_rect_area, get_image_paths_from_folder, BTN_X_FOLDER, ERROR_FOLDER
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

MAX_ZOOM_CLICKS = 5
CITY_HEIGHT = 80
CITY_WIDTH = 120
HEIGHT_OFFSET = 70
INVEST_MINUTES_TO_RECHECK = 180

MAP_FOLDER = "data/map"
MAP_CENTER_FILES = get_image_paths_from_folder(MAP_FOLDER + "/center")
MAP_ZOOM_IN_FILES = get_image_paths_from_folder(MAP_FOLDER + "/zoom_in")

CITY_FOLDER = "data/city"
CITY_GO_LEFT_FILES = get_image_paths_from_folder(CITY_FOLDER + "/go_left")
CITY_GO_RIGHT_FILES = get_image_paths_from_folder(CITY_FOLDER + "/go_right")
CITY_PROJECT_FILES = get_image_paths_from_folder(CITY_FOLDER + "/city_project")
USER_LABEL_FILES = get_image_paths_from_folder(CITY_FOLDER + "/user_label")
CONTRIBUTE_COIN_ICON_FILES = get_image_paths_from_folder(CITY_FOLDER + "/contribute_coin_icon")
CONTRIBUTE_BAR_FILES = get_image_paths_from_folder(CITY_FOLDER + "/contribute_bar")
CONTRIBUTE_HEADER_FILES = get_image_paths_from_folder(CITY_FOLDER + "/contribute_header")

TEMP_CITY_LABEL = "start_city_label.png"

logging.basicConfig(level=logging.INFO)


def get_city_label():
    logging.debug("start CityInvest.get_city_label")
    left_on_screen, left_position, _, left_image = any_image_on_screen(CITY_GO_LEFT_FILES)
    right_on_screen, right_position, _, right_image = any_image_on_screen(CITY_GO_RIGHT_FILES)

    if not left_on_screen and not right_on_screen:
        get_screenshot(save=True, filename=f"{ERROR_FOLDER}/get_city_label_fail")
        raise ImageNotFoundException("Fail get city label.")

    left_width, _ = get_image_size(left_image)
    _, right_height = get_image_size(right_image)

    x_start = left_position[0] + left_width
    y_start = left_position[1]
    x_finish = right_position[0]
    y_finish = right_position[1] + right_height
    boundaries = (x_start, y_start, x_finish, y_finish)

    full_screenshot = get_screenshot()
    city_label = full_screenshot.crop(boundaries)

    return city_label


def get_screenshot_contribute_pop_up():
    logging.debug("start CityInvest.get_screenshot_contribute_pop_up")
    screenshot = get_screenshot()
    on_screen, position, _, _ = any_image_on_screen(CONTRIBUTE_HEADER_FILES, screenshot=screenshot)
    if not on_screen:
        get_screenshot(save=True, filename=f"{ERROR_FOLDER}/contribute_header_not_found")
        raise ImageNotFoundException("Failed to find header on screen for city project")
    top_left_corner = (0, position[1])
    screenshot_width, screenshot_height = screenshot.size
    size = (screenshot_width, screenshot_height - position[1])
    screenshot_contribute_pop_up = get_screenshot_with_black_out_of_box(top_left_corner, size)
    return screenshot_contribute_pop_up


class CityInvest(RailRunnable):

    def __init__(self):
        super().__init__()
        self.task_name = self.__class__.__name__
        self.next_run_time = datetime.datetime.now()
        self.sleep_center_city = 10
        self.sleep_zoom = 2
        self.sleep_select_city = 10
        self.sleep_select_subtab_city_project = 5
        self.sleep_donate = 5
        self.sleep_select_next_city = 5

    def _run(self):
        self._run_city_invest()

    def _update_next_run_time(self):
        logging.debug("start CityInvest._update_next_run_time")
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.debug(f"Next {self.__class__.__name__} at {target_datetime.time()}")

    def _run_city_invest(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.WORLD_MAP.value)
        self._center_and_zoom_to_city()
        self._select_city()
        self._select_subtab_city_project()
        self._check_all_cities()

    def _center_and_zoom_to_city(self):
        logging.debug("start CityInvest._center_and_zoom_to_city")
        close_all_pop_ups()
        self._zoom_max()
        self._center_map()

    def _zoom_max(self):
        on_screen, _, _, _ = any_image_on_screen(MAP_ZOOM_IN_FILES)
        tries = 0
        while on_screen and tries < MAX_ZOOM_CLICKS:
            tries += 1
            self._zoom_once()
            on_screen, _, _, _ = any_image_on_screen(MAP_ZOOM_IN_FILES)

    def _zoom_once(self):
        find_image_and_click(MAP_ZOOM_IN_FILES,
                             msg="zoom",
                             error_filename="fail_zoom_once")
        sleep_random(self.sleep_zoom / 2)
        move_mouse_close_to_center()
        sleep_random(self.sleep_zoom / 2)

    def _center_map(self):
        find_image_and_click(MAP_CENTER_FILES,
                             msg="center map",
                             error_filename="fail_center_map")
        sleep_random(self.sleep_center_city)

    def _select_city(self):
        logging.debug("start CityInvest._select_city")
        screen_width, screen_height = pyautogui.size()
        top_left_corner = ((screen_width - CITY_WIDTH) // 2, (screen_height + HEIGHT_OFFSET - CITY_HEIGHT) // 2)
        size = (CITY_WIDTH, CITY_HEIGHT)
        click_on_rect_area(top_left_corner, size)

        sleep_random(self.sleep_select_city)

    def _select_subtab_city_project(self):
        logging.debug("start CityInvest._select_subtab_city_project")
        find_image_and_click(CITY_PROJECT_FILES,
                             msg="subtab city project",
                             error_filename="fail_select_subtab_city_project")
        sleep_random(self.sleep_select_subtab_city_project)

    def _check_all_cities(self):
        logging.debug("start CityInvest._check_all_cities")
        start_city_label = get_city_label()
        start_city_label_filename = CITY_FOLDER + "/" + TEMP_CITY_LABEL
        start_city_label.save(start_city_label_filename)
        on_screen = False
        while not on_screen:
            self._donate_if_needed()
            self._select_next_city()
            on_screen, _, _ = image_on_screen(start_city_label_filename)

    def _donate_if_needed(self):
        logging.debug("start CityInvest._donate_if_needed")
        have_contributions, _, _, _ = any_image_on_screen(USER_LABEL_FILES)
        if not have_contributions:
            logging.debug("Need donation")
            find_image_and_click(CONTRIBUTE_COIN_ICON_FILES,
                                 msg="city contribute",
                                 error_filename="fail_select_donate_if_needed_CONTRIBUTE_COIN_ICON_FILES")
            find_image_and_click(CONTRIBUTE_BAR_FILES,
                                 msg="city contribute sub btn",
                                 error_filename="fail_select_donate_if_needed_CONTRIBUTE_BAR_FILES")
            screenshot_contribute_pop_up = get_screenshot_contribute_pop_up()

            x_close_img_paths = get_image_paths_from_folder(BTN_X_FOLDER)
            find_image_and_click(x_close_img_paths,
                                 screenshot=screenshot_contribute_pop_up,
                                 msg="close city contribute pop-up",
                                 error_filename="fail_select_donate_if_needed_BTN_X_FOLDER")
            sleep_random(self.sleep_donate)
        else:
            logging.debug("No need donation")

    def _select_next_city(self):
        logging.debug("start CityInvest._select_next_city")
        find_image_and_click(CITY_GO_RIGHT_FILES,
                             msg="next city",
                             error_filename="fail_select_next_city")
        sleep_random(self.sleep_select_next_city)
