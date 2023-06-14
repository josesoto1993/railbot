import datetime
import logging

from rail_utils.rail_utils import sleep_random, find_image_and_click

INVEST_MINUTES_TO_RECHECK = 60


def center_city(sleep_time=10):
    logging.error("Implement center_city")
    sleep_random(sleep_time)


def select_city(sleep_time=10):
    logging.error("Implement select_city")
    sleep_random(sleep_time)


def select_subtab_city_project(sleep_time=10):
    logging.error("Implement select_subtab_city_project")
    sleep_random(sleep_time)


def get_city_label(sleep_time=10):
    logging.error("Implement get_city_label")
    sleep_random(sleep_time)
    return 1


def donate_if_needed(sleep_time=10):
    logging.error("Implement donate_if_needed")
    sleep_random(sleep_time)


def select_next_city(sleep_time=10):
    logging.error("Implement select_next_city")
    sleep_random(sleep_time)


class CityInvest:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_center_city = 3
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
        center_city(self.sleep_center_city)
        select_city(self.sleep_select_city)
        select_subtab_city_project(self.sleep_select_subtab_city_project)
        self._check_all_cities()

    def _check_all_cities(self):
        start_city = get_city_label()
        current_city = None
        while current_city != start_city:
            donate_if_needed(self.sleep_donate_if_needed)
            select_next_city(self.sleep_select_next_city)
            current_city = get_city_label()

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next city invest at {target_datetime.time()} -----")
