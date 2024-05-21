import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import any_image_on_screen, ImageNotFoundException, timestamped_filename, get_screenshot, \
    click_on_rect_area, sleep_random, get_image_size, ERROR_FOLDER
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

BONUS_MINUTES_TO_RECHECK = 3

# TODO: revisar toda la carpeta data/widget y verificar se usan todas las imagenes
# TODO: esto esta super viejo, la carpeta no debe ir aqui, lo archivos se deben cargar por carpeta
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
        super().__init__()
        self.task_name = self.__class__.__name__
        self.next_run_time = datetime.datetime.now()
        self.sleep_open_widget = 3

    def _run(self):
        self._run_building_bonus()

    def _update_next_run_time(self):
        self.next_run_time = datetime.datetime.now() + datetime.timedelta(minutes=BONUS_MINUTES_TO_RECHECK)
        logging.debug(f"Next {self.__class__.__name__} at {self.next_run_time.time()}")

    def _run_building_bonus(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.WORLD_MAP.value)
        self._open_or_reopen_widget()

    def _open_or_reopen_widget(self):
        on_screen, position, _, image_path = any_image_on_screen(ALL_WIDGET)
        if not on_screen:
            filename = timestamped_filename(filename=f"{ERROR_FOLDER}/error_widget")
            get_screenshot(save=True, filename=filename)
            raise ImageNotFoundException(f"Fail find any widget for images: {ALL_WIDGET}")

        self._open_or_reopen_widget_handle_click(image_path, position)

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

    def _open_or_reopen_widget_handle_click(self, image_path, position):
        width, height = get_image_size(image_path)
        size_to_click = width, height * 4 // 10
        click_on_rect_area(position, size=size_to_click)
        sleep_random(self.sleep_open_widget)
        if image_path == WIDGET_SELECTED or image_path == WIDGET_SELECTED_SMALL:
            click_on_rect_area(position, size=size_to_click)
            sleep_random(self.sleep_open_widget)
