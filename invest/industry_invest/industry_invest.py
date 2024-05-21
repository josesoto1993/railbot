import datetime
import logging

from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, sleep_random, move_mouse_close_to_center, any_image_on_screen, \
    get_image_paths_from_folder, ERROR_FOLDER, get_screenshot
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVEST_MINUTES_TO_RECHECK = 180

RANKING_FOLDER = "data/tab_ranking"
RANKING_INDUSTRIES_FILES = get_image_paths_from_folder(RANKING_FOLDER + "/ranking_industries")
RANKING_INDUSTRIES_INVEST_FILES = get_image_paths_from_folder(RANKING_FOLDER + "/ranking_industries_invest")
RANKING_SHOW_MORE_FILES = get_image_paths_from_folder(RANKING_FOLDER + "/show_more")
RANKING_INVEST_ZERO_FILES = get_image_paths_from_folder(RANKING_FOLDER + "/invest_zero")

INDUSTRY_FOLDER = "data/industry"
INDUSTRY_INVEST_FILES = get_image_paths_from_folder(INDUSTRY_FOLDER + "/invest")

logging.basicConfig(level=logging.INFO)


class IndustryInvest(RailRunnable):
    def __init__(self):
        super().__init__()
        self.task_name = self.__class__.__name__
        self.next_run_time = datetime.datetime.now()
        self.sleep_select_subtab_industries = 5
        self.sleep_select_subsubtab_invest = 10
        self.sleep_show_last = 2
        self.sleep_select_zero_investment = 5
        self.sleep_industry_invest = 5
        self.invest_done = False

    def _run(self):
        self._run_industry_invest()

    def _update_next_run_time(self, invest_done=True):
        if self.invest_done:
            logging.debug("May have more industries to invest, next loop invest another one")
        else:
            target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

            self.next_run_time = target_datetime
            logging.debug(f"Next {self.__class__.__name__} at {target_datetime.time()}")

    def _run_industry_invest(self):
        logging.debug(f"Run {self.__class__.__name__}: Start at {datetime.datetime.now().time()}")
        open_tab(Tabs.RANKINGS.value)
        self._select_subtab_industries()
        self._select_subsubtab_invest()
        self._show_last()
        self.invest_done = self._invest_if_needed()

    def _select_subtab_industries(self):
        find_image_and_click(RANKING_INDUSTRIES_FILES,
                             msg="subtab industries",
                             error_filename="fail_select_subtab_industries")
        sleep_random(self.sleep_select_subtab_industries)

    def _select_subsubtab_invest(self):
        find_image_and_click(RANKING_INDUSTRIES_INVEST_FILES,
                             msg="subsubtab invest",
                             error_filename="fail_select_subsubtab_invest")
        sleep_random(self.sleep_select_subsubtab_invest)

    def _show_last(self):
        precision = 0.95
        on_screen, _, _, _ = any_image_on_screen(RANKING_SHOW_MORE_FILES, precision=precision)

        if not on_screen:
            get_screenshot(save=True, filename=f"{ERROR_FOLDER}/warning_cant_find_show_more_on_initial_ranking")
            return

        while on_screen:
            find_image_and_click(RANKING_SHOW_MORE_FILES,
                                 msg="show more",
                                 precision=precision,
                                 error_filename="fail_show_last")
            sleep_random(self.sleep_show_last / 2)
            move_mouse_close_to_center()
            sleep_random(self.sleep_show_last / 2)
            on_screen, _, _, _ = any_image_on_screen(RANKING_SHOW_MORE_FILES, precision=precision)

    def _invest_if_needed(self):
        any_zero_invest_industry = self._select_zero_investment()
        if not any_zero_invest_industry:
            return False
        self._industry_invest()
        return True

    def _select_zero_investment(self):
        invest_precision = 0.9
        on_screen, _, _, _ = any_image_on_screen(RANKING_INVEST_ZERO_FILES,
                                                 precision=invest_precision)
        if on_screen:
            find_image_and_click(RANKING_INVEST_ZERO_FILES,
                                 precision=invest_precision,
                                 msg="zero investment",
                                 error_filename="fail_select_zero_investment")
            sleep_random(self.sleep_select_zero_investment)
            return True
        else:
            logging.debug("Nothing to invest, no one with zero")
            return False

    def _industry_invest(self):
        find_image_and_click(INDUSTRY_INVEST_FILES,
                             msg="invest",
                             error_filename="fail_industry_invest")
        sleep_random(self.sleep_industry_invest)
