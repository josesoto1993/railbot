import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import any_image_on_screen, ImageNotFoundException, timestamped_filename, get_screenshot, \
    click_on_rect_area, sleep_random, get_image_size
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

BONUS_MINUTES_TO_RECHECK = 3

WIDGET_FOLDER = "data/widget"
WIDGET_BASE = WIDGET_FOLDER + "/widget_base.png"
WIDGET_BASE_SMALL = WIDGET_FOLDER + "/widget_base_small.png"
WIDGET_SELECTED = WIDGET_FOLDER + "/widget_selected.png"
WIDGET_SELECTED_SMALL = WIDGET_FOLDER + "/widget_selected_small.png"
ALL_WIDGET = [WIDGET_BASE,
              WIDGET_BASE_SMALL,
              WIDGET_SELECTED,
              WIDGET_SELECTED_SMALL]


class BuildingBonus(RailRunnable):
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_open_widget = 3

    def run(self) -> datetime:
        if self._should_run():
            self._run_building_bonus()
            self._update_next_run_time()
        return self.next_run_time

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_building_bonus(self):
        logging.info(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.WORLD_MAP.value)
        self._open_or_reopen_widget()

    def _open_or_reopen_widget(self):
        on_screen, position, _, image_path = any_image_on_screen(ALL_WIDGET, precision=0.8)
        if not on_screen:
            filename = timestamped_filename(filename="errors/error_widget")
            get_screenshot(save=True, filename=filename)
            raise ImageNotFoundException(f"Fail find any widget for images: {ALL_WIDGET}")

        self._open_or_reopen_widget_handle_click(image_path, position)

    def _open_or_reopen_widget_handle_click(self, image_path, position):
        width, height = get_image_size(image_path)
        size_to_click = width, height * 4 // 10
        click_on_rect_area(position, size=size_to_click)
        sleep_random(self.sleep_open_widget)
        if image_path == WIDGET_SELECTED or image_path == WIDGET_SELECTED_SMALL:
            click_on_rect_area(position, size=size_to_click)
            sleep_random(self.sleep_open_widget)

    def _update_next_run_time(self):
        self.next_run_time = datetime.datetime.now() + datetime.timedelta(minutes=BONUS_MINUTES_TO_RECHECK)
        logging.info(f"Next {self.__class__.__name__} at {self.next_run_time.time()}")

# open world map
# close all
# check / open widget
# check / open association widget
# reload association bonus (just in case..)
# while money symbol on screen:
#   claim bonus (click image)
#   wait
#   close if needed
#   money symbol on screen
# while pp symbol on screen:
#   claim bonus (click image)
#   wait
#   close if needed
#   pp symbol on screen
