import datetime
import logging

import pyautogui

from rail_utils.rail_utils import any_image_on_screen, image_on_screen, ImageNotFoundException, get_image_size, \
    get_screenshot, get_screenshot_with_black_out_of_box, close_all_pop_ups, sleep_random, find_image_and_click, \
    move_mouse_close_to_center, click_on_rect_area, GENERAL_BTN_X
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

MAX_ZOOM_CLICKS = 5
CITY_HEIGHT = 80
CITY_WIDTH = 120
HEIGHT_OFFSET = 70
INVEST_MINUTES_TO_RECHECK = 180

MAP_FOLDER = "data/map"
MAP_BTN_CENTER = MAP_FOLDER + "/btn_center.png"
MAP_BTN_CENTER_SMALL = MAP_FOLDER + "/btn_center_small.png"
CENTER_MAP_BTN = [MAP_BTN_CENTER, MAP_BTN_CENTER_SMALL]
BTN_ZOOM_IN_BASE = MAP_FOLDER + "/btn_zoom_in_base.png"
BTN_ZOOM_IN_BASE_SMALL = MAP_FOLDER + "/btn_zoom_in_base_small.png"
ZOOM_IN_BTN = [BTN_ZOOM_IN_BASE, BTN_ZOOM_IN_BASE_SMALL]

CITY_FOLDER = "data/city"
CITY_SUBTAB_CITY_PROJECT = CITY_FOLDER + "/city_subtab_city_project.png"
CITY_SUBTAB_CITY_PROJECT_SMALL = CITY_FOLDER + "/city_subtab_city_project_small.png"
CITY_PROJECT_SUBTAB_BTN = [CITY_SUBTAB_CITY_PROJECT,
                           CITY_SUBTAB_CITY_PROJECT_SMALL]
CITY_LABEL_LEFT = CITY_FOLDER + "/city_label_left.png"
CITY_LABEL_LEFT_SMALL = CITY_FOLDER + "/city_label_left_small.png"
CITY_LEFT_ARROW = [CITY_LABEL_LEFT,
                   CITY_LABEL_LEFT_SMALL]
CITY_LABEL_RIGHT = CITY_FOLDER + "/city_label_right.png"
CITY_LABEL_RIGHT_SMALL = CITY_FOLDER + "/city_label_right_small.png"
CITY_RIGHT_ARROW = [CITY_LABEL_RIGHT,
                    CITY_LABEL_RIGHT_SMALL]
USER_LABEL = CITY_FOLDER + "/user_donation_label.png"
USER_LABEL_SMALL = CITY_FOLDER + "/user_donation_label_small.png"
USER_DONATE_LABEL = [USER_LABEL,
                     USER_LABEL_SMALL]
CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE = CITY_FOLDER + "/city_subtab_city_project_contribute.png"
CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_SMALL = CITY_FOLDER + "/city_subtab_city_project_contribute_small.png"
CITY_CONTRIBUTE_BTN = [CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE,
                       CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_SMALL]
CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_HEADER = CITY_FOLDER + "/city_subtab_city_project_contribute_header.png"
CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_HEADER_SMALL = CITY_FOLDER + "/city_subtab_city_project_contribute_header_small.png"
POPUP_CONTRIBUTE_HEADER = [CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_HEADER,
                           CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_HEADER_SMALL]
CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_BTN = CITY_FOLDER + "/city_subtab_city_project_contribute_btn.png"
CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_BTN_SMALL = CITY_FOLDER + "/city_subtab_city_project_contribute_btn_small.png"
POPUP_CONTRIBUTE_BTN = [CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_BTN,
                        CITY_SUBTAB_CITY_PROJECT_CONTRIBUTE_BTN_SMALL]

TEMP_CITY_LABEL = "start_city_label.png"

logging.basicConfig(level=logging.INFO)


def get_city_label():
    logging.debug(f"start CityInvest.get_city_label")
    left_on_screen, left_position, _, left_image = any_image_on_screen(CITY_LEFT_ARROW)
    right_on_screen, right_position, _, right_image = any_image_on_screen(CITY_RIGHT_ARROW)

    if not left_on_screen and not right_on_screen:
        raise ImageNotFoundException(f"Fail cet city label.")

    left_width, left_height = get_image_size(left_image)
    right_width, right_height = get_image_size(right_image)

    x_start = left_position[0] + left_width
    y_start = left_position[1]
    x_finish = right_position[0]
    y_finish = right_position[1] + right_height
    boundaries = (x_start, y_start, x_finish, y_finish)

    full_screenshot = get_screenshot()
    city_label = full_screenshot.crop(boundaries)

    return city_label


def get_screenshot_contribute_pop_up():
    logging.debug(f"start CityInvest.get_screenshot_contribute_pop_up")
    screenshot = get_screenshot()
    on_screen, position, _, _ = any_image_on_screen(POPUP_CONTRIBUTE_HEADER, screenshot=screenshot)
    if not on_screen:
        raise ImageNotFoundException(
            f"Failed to find header on screen for city project")
    top_left_corner = (0, position[1])
    screenshot_width, screenshot_height = screenshot.size
    size = (screenshot_width, screenshot_height - position[1])
    screenshot_contribute_pop_up = get_screenshot_with_black_out_of_box(top_left_corner, size)
    return screenshot_contribute_pop_up


class CityInvest:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_center_city = 10
        self.sleep_zoom = 2
        self.sleep_select_city = 10
        self.sleep_select_subtab_city_project = 5
        self.sleep_donate = 5
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
        logging.info(f"----- Run city invest: Start at {datetime.datetime.now().time()} -----")
        open_tab(Tabs.WORLD_MAP.value)
        self._center_and_zoom_to_city()
        self._select_city()
        self._select_subtab_city_project()
        self._check_all_cities()

    def _center_and_zoom_to_city(self):
        logging.debug(f"start CityInvest._center_and_zoom_to_city")
        close_all_pop_ups()
        self._zoom_max()
        self._center_map()

    def _zoom_max(self):
        precision = 0.95
        on_screen, position, _, _ = any_image_on_screen(ZOOM_IN_BTN, precision=precision)
        tries = 0
        while on_screen and tries < MAX_ZOOM_CLICKS:
            tries += 1
            self._zoom_once()
            on_screen, position, _, _ = any_image_on_screen(ZOOM_IN_BTN, precision=precision)

    def _zoom_once(self):
        find_image_and_click(ZOOM_IN_BTN, msg="zoom")
        sleep_random(self.sleep_zoom / 2)
        move_mouse_close_to_center()
        sleep_random(self.sleep_zoom / 2)

    def _center_map(self):
        find_image_and_click(CENTER_MAP_BTN, msg="center map")
        sleep_random(self.sleep_center_city)

    def _select_city(self):
        logging.debug(f"start CityInvest._select_city")
        screen_width, screen_height = pyautogui.size()
        top_left_corner = ((screen_width - CITY_WIDTH) // 2, (screen_height + HEIGHT_OFFSET - CITY_HEIGHT) // 2)
        size = (CITY_WIDTH, CITY_HEIGHT)
        click_on_rect_area(top_left_corner, size)

        sleep_random(self.sleep_select_city)

    def _select_subtab_city_project(self):
        logging.debug(f"start CityInvest._select_subtab_city_project")
        find_image_and_click(CITY_PROJECT_SUBTAB_BTN, msg="subtab city project")
        sleep_random(self.sleep_select_subtab_city_project)

    def _check_all_cities(self):
        logging.debug(f"start CityInvest._check_all_cities")
        start_city_label = get_city_label()
        start_city_label_filename = CITY_FOLDER + "/" + TEMP_CITY_LABEL
        start_city_label.save(start_city_label_filename)
        on_screen = False
        while not on_screen:
            self._donate_if_needed()
            self._select_next_city()
            on_screen, position, _ = image_on_screen(start_city_label_filename)

    def _donate_if_needed(self):
        logging.debug(f"start CityInvest._donate_if_needed")
        have_contributions, _, _, _ = any_image_on_screen(USER_DONATE_LABEL)
        if not have_contributions:
            find_image_and_click(CITY_CONTRIBUTE_BTN, msg="city contribute")
            find_image_and_click(POPUP_CONTRIBUTE_BTN, msg="city contribute sub btn")
            screenshot_contribute_pop_up = get_screenshot_contribute_pop_up()
            find_image_and_click(GENERAL_BTN_X, screenshot=screenshot_contribute_pop_up,
                                 msg="close city contribute pop-up")
            sleep_random(self.sleep_donate)
        else:
            logging.debug(f"No need donation")

    def _select_next_city(self):
        logging.debug(f"start CityInvest._select_next_city")
        find_image_and_click(CITY_RIGHT_ARROW, msg="next city")
        sleep_random(self.sleep_select_next_city)

    def _update_next_run_time(self):
        logging.debug(f"start CityInvest._update_next_run_time")
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next city invest at {target_datetime.time()} -----")
