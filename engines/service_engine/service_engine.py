import datetime
import logging

from rail_utils.folders_paths import TAB_ENGINE_FOLDER
from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import sleep_random, find_image_and_click, any_image_on_screen, get_image_paths_from_folder, \
    ERROR_FOLDER, get_screenshot, ImageNotFoundException
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

SERVICE_ENGINE_MINUTES_TO_RECHECK = 90

logging.basicConfig(level=logging.INFO)


class ServiceEngine(RailRunnable):
    def __init__(self):
        super().__init__()
        self.task_name = self.__class__.__name__
        self.sleep_service_multiple = 5
        self.sleep_all_needing_service = 3
        self.sleep_service_all = 10
        self.next_run_time = datetime.datetime.now()

    def _run(self):
        self._run_service()

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=SERVICE_ENGINE_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.debug(f"Next {self.__class__.__name__} at {target_datetime.time()}")

    def _run_service(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.ENGINES.value)
        self._select_service_multiple()
        self._select_all_needing_service()
        self._select_service_all()

    def _select_service_multiple(self):
        service_multiple_files = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/service_multiple")
        find_image_and_click(service_multiple_files,
                             msg="service multiple btn",
                             error_filename="fail_select_service_multiple")
        sleep_random(self.sleep_service_multiple)

    def _select_all_needing_service(self):
        all_needing_service_files = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/all_needing_service")
        find_image_and_click(all_needing_service_files,
                             msg="all needing service btn",
                             error_filename="fail_select_all_needing_service")
        sleep_random(self.sleep_all_needing_service)

    def _select_service_all(self):
        service_all_label_files = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/service_all")
        service_unavailable_label_files = get_image_paths_from_folder(TAB_ENGINE_FOLDER + "/service_unavailable")

        on_screen_service_all, _, _, _ = any_image_on_screen(service_all_label_files)
        on_screen_service_unavailable, _, _, _ = any_image_on_screen(service_unavailable_label_files)

        if on_screen_service_all:
            find_image_and_click(service_all_label_files,
                                 msg="service all",
                                 error_filename="fail_select_service_all")
            sleep_random(self.sleep_service_all)
        elif on_screen_service_unavailable:
            logging.debug("No need to service any engine")
        else:
            get_screenshot(save=True, filename=f"{ERROR_FOLDER}/service_all_or_none_not_found")
            raise ImageNotFoundException("Service all or none not found")
