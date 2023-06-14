import datetime
import logging

import pyautogui

from rail_utils.rail_utils import find_image_and_click, sleep_random, image_on_screen, \
    move_mouse_close_to_center
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVEST_MINUTES_TO_RECHECK = 60
RANKING_SUBTAB_INDUSTRIES = "data/tab_ranking/ranking_subtab_industries_base.png"
RANKING_SUBSUBTAB_INVEST = "data/tab_ranking/ranking_subtab_industries_invest_base.png"
RANKING_SHOW_MORE = "data/tab_ranking/ranking_subtab_industries_show_more_base.png"
RANKING_SUBSUBTAB_INVEST_ZERO = "data/tab_ranking/ranking_subtab_industries_invest_zero_base.png"
INDUSTRY_INVEST_BASE = "data/industry/industry_invest_base.png"
INDUSTRY_INVEST_VOUCHER_BASE = "data/industry/industry_invest_voucher_base.png"

logging.basicConfig(level=logging.INFO)


def select_subtab_industries(sleep_time=10):
    find_image_and_click([RANKING_SUBTAB_INDUSTRIES],
                         on_screen_msg="Select subtab industries",
                         on_fail_msg="Fail select subtab industries")
    sleep_random(sleep_time)


def select_subsubtab_invest(sleep_time=10):
    find_image_and_click([RANKING_SUBSUBTAB_INVEST],
                         on_screen_msg="Select subsubtab invest",
                         on_fail_msg="Fail select subsubtab invest")
    sleep_random(sleep_time)


def show_last(sleep_time=10):
    on_screen = True
    while on_screen:
        find_image_and_click([RANKING_SHOW_MORE],
                             on_screen_msg="Select show more",
                             on_fail_msg="Fail select show more")
        sleep_random(sleep_time / 2)
        move_mouse_close_to_center()
        sleep_random(sleep_time / 2)
        on_screen, position = image_on_screen(RANKING_SHOW_MORE, precision=0.9)


def select_zero_investment(sleep_time=10):
    on_screen, position = image_on_screen(RANKING_SUBSUBTAB_INVEST_ZERO, precision=0.95)
    if on_screen:
        find_image_and_click([RANKING_SUBSUBTAB_INVEST_ZERO],
                             on_screen_msg="Select zero investment",
                             on_fail_msg="Fail select zero investment")
        sleep_random(sleep_time)
        return True
    else:
        logging.info("Nothing to invest, no one with zero")
        return False


def industry_invest(sleep_time=10):
    find_image_and_click([INDUSTRY_INVEST_BASE, INDUSTRY_INVEST_VOUCHER_BASE],
                         on_screen_msg="Select invest",
                         on_fail_msg="Fail select invest")
    sleep_random(sleep_time)


def get_screenshot_only_left_bottom():
    screenshot = pyautogui.screenshot()

    width, height = screenshot.size

    pixels = screenshot.load()

    for y in range(height):
        for x in range(width // 2, width):
            pixels[x, y] = (0, 0, 0)

    for y in range(0, height // 2):
        for x in range(width):
            pixels[x, y] = (0, 0, 0)

    return screenshot


class IndustryInvest:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_select_subtab_industries = 5
        self.sleep_select_subsubtab_invest = 10
        self.sleep_show_last = 2
        self.sleep_select_zero_investment = 5
        self.sleep_industry_invest = 5

    def run(self):
        if self._should_run():
            try:
                invest_done = self._run_invest()
                self._update_next_run_time(invest_done)
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_invest(self):
        logging.info(f"----- Run industry invest: Start -----")
        open_tab(Tabs.RANKINGS)
        select_subtab_industries(self.sleep_select_subtab_industries)
        select_subsubtab_invest(self.sleep_select_subsubtab_invest)
        show_last(self.sleep_show_last)
        any_zero_invest_industry = select_zero_investment(self.sleep_select_zero_investment)
        if not any_zero_invest_industry:
            return False
        industry_invest(self.sleep_industry_invest)
        return True

    def _update_next_run_time(self, invest_done=True):
        if invest_done:
            logging.info(f"----- May have more industries to invest, next loop invest another one -----")
        else:
            target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

            self.next_run_time = target_datetime
            logging.info(f"----- Next industry invest at {target_datetime.time()} -----")
