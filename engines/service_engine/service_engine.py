import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import sleep_random, find_image_and_click, any_image_on_screen, get_image_paths_from_folder
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

SERVICE_ENGINE_MINUTES_TO_RECHECK = 90

TAB_ENGINE_FOLDER = "data/tab_engine"

SERVICE_MULTIPLE_FILES = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/all_needing_service")
ALL_NEEDING_SERVICE_FILES = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/service_all")
SERVICE_ALL_LABEL_FILES = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/service_multiple")

logging.basicConfig(level=logging.INFO)


class ServiceEngine(RailRunnable):
    def __init__(self):
        self.sleep_service_multiple = 5
        self.sleep_all_needing_service = 3
        self.sleep_service_all = 10
        self.next_run_time = datetime.datetime.now()

    def run(self) -> datetime:
        if self._should_run():
            self._run_service()
            self._update_next_run_time()
        return self.next_run_time

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_service(self):
        logging.info(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.ENGINES.value)
        self._select_service_multiple()
        self._select_all_needing_service()
        self._select_service_all()

    def _select_service_multiple(self):
        find_image_and_click(SERVICE_MULTIPLE_FILES,
                             msg="service multiple btn",
                             error_filename="fail_select_service_multiple")
        sleep_random(self.sleep_service_multiple)

    def _select_all_needing_service(self):
        find_image_and_click(ALL_NEEDING_SERVICE_FILES,
                             msg="all needing service btn",
                             error_filename="fail_select_all_needing_service")
        sleep_random(self.sleep_all_needing_service)

    def _select_service_all(self):
        on_screen, _, _, _ = any_image_on_screen(SERVICE_ALL_LABEL_FILES)
        if on_screen:
            find_image_and_click(SERVICE_ALL_LABEL_FILES,
                                 msg="service all",
                                 error_filename="fail_select_service_all")
            sleep_random(self.sleep_service_all)
        else:
            logging.debug("No need to service any engine")

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=SERVICE_ENGINE_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"Next {self.__class__.__name__} at {target_datetime.time()}")
