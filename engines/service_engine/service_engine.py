import datetime
import logging

from rail_utils.rail_utils import sleep_random, find_image_and_click, image_on_screen
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

SERVICE_ENGINE_MINUTES_TO_RECHECK = 90
SERVICE_MULTIPLE_BTN = "data/tab_engine/service_multiple_btn.png"
ALL_NEEDING_SERVICE_BTN = "data/tab_engine/all_needing_service_btn.png"
SERVICE_ALL_LABEL = "data/tab_engine/service_all_label.png"

logging.basicConfig(level=logging.INFO)


class ServiceEngine:
    def __init__(self):
        self.sleep_service_multiple = 5
        self.sleep_all_needing_service = 3
        self.sleep_service_all = 10
        self.next_run_time = datetime.datetime.now()

    def run(self):
        if self._should_run():
            try:
                self._run_service()
                self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_service(self):
        logging.info(f"----- Run service engine: Start -----")
        open_tab(Tabs.ENGINES)
        self._select_service_multiple()  # 5s
        self._select_all_needing_service()  # 3s
        self._select_service_all()  # 10s

        return

    def _select_service_multiple(self):
        find_image_and_click([SERVICE_MULTIPLE_BTN], msg="service multiple btn")
        sleep_random(self.sleep_service_multiple)

    def _select_all_needing_service(self):
        find_image_and_click([ALL_NEEDING_SERVICE_BTN], msg="all needing service btn")
        sleep_random(self.sleep_all_needing_service)

    def _select_service_all(self):
        on_screen, position = image_on_screen(SERVICE_ALL_LABEL)
        if on_screen:
            find_image_and_click([SERVICE_ALL_LABEL], msg="service all")
            sleep_random(self.sleep_service_all)
        else:
            logging.info(f"No need to service any engine")

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=SERVICE_ENGINE_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next service engine at {target_datetime.time()} -----")
