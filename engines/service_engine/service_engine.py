import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import sleep_random, find_image_and_click, any_image_on_screen
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

SERVICE_ENGINE_MINUTES_TO_RECHECK = 90

SERVICE_MULTIPLE_BTN = "data/tab_engine/service_multiple_btn.png"
SERVICE_MULTIPLE_BTN_SMALL = "data/tab_engine/service_multiple_btn_small.png"
ALL_NEEDING_SERVICE_BTN = "data/tab_engine/all_needing_service_btn.png"
ALL_NEEDING_SERVICE_BTN_SMALL = "data/tab_engine/all_needing_service_btn_small.png"
SERVICE_ALL_LABEL = "data/tab_engine/service_all_label.png"
SERVICE_ALL_LABEL_SMALL = "data/tab_engine/service_all_label_small.png"

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
        logging.info(f"----- Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()} -----")
        open_tab(Tabs.ENGINES.value)
        self._select_service_multiple()
        self._select_all_needing_service()
        self._select_service_all()

    def _select_service_multiple(self):
        service_multiple_btn = [SERVICE_MULTIPLE_BTN, SERVICE_MULTIPLE_BTN_SMALL]
        find_image_and_click(service_multiple_btn, msg="service multiple btn")
        sleep_random(self.sleep_service_multiple)

    def _select_all_needing_service(self):
        all_needing_service_btn = [ALL_NEEDING_SERVICE_BTN, ALL_NEEDING_SERVICE_BTN_SMALL]
        find_image_and_click(all_needing_service_btn, msg="all needing service btn")
        sleep_random(self.sleep_all_needing_service)

    def _select_service_all(self):
        service_all_label = [SERVICE_ALL_LABEL, SERVICE_ALL_LABEL_SMALL]
        on_screen, _, _, _ = any_image_on_screen(service_all_label)
        if on_screen:
            find_image_and_click(service_all_label, msg="service all")
            sleep_random(self.sleep_service_all)
        else:
            logging.debug("No need to service any engine")

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=SERVICE_ENGINE_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next {self.__class__.__name__} at {target_datetime.time()} -----")
