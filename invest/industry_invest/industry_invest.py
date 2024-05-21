import datetime
import logging

from rail_utils.folders_paths import RANKING_FOLDER, INDUSTRY_FOLDER, ERROR_FOLDER
from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import find_image_and_click, sleep_random, move_mouse_close_to_center, any_image_on_screen, \
    get_image_paths_from_folder, get_screenshot
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVEST_MINUTES_TO_RE_RUN = 1
INVEST_MINUTES_TO_RECHECK = 180

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
            target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RE_RUN)
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
        ranking_industries_files = get_image_paths_from_folder(RANKING_FOLDER + "/ranking_industries")
        find_image_and_click(ranking_industries_files,
                             msg="subtab industries",
                             error_filename="fail_select_subtab_industries")
        sleep_random(self.sleep_select_subtab_industries)

    def _select_subsubtab_invest(self):
        ranking_industries_invest_files = get_image_paths_from_folder(RANKING_FOLDER + "/ranking_industries_invest")
        find_image_and_click(ranking_industries_invest_files,
                             msg="subsubtab invest",
                             error_filename="fail_select_subsubtab_invest")
        sleep_random(self.sleep_select_subsubtab_invest)

    def _show_last(self):
        precision = 0.95
        ranking_show_more_files = get_image_paths_from_folder(RANKING_FOLDER + "/show_more")
        on_screen, _, _, _ = any_image_on_screen(ranking_show_more_files, precision=precision)

        if not on_screen:
            get_screenshot(save=True, filename=f"{ERROR_FOLDER}/warning_cant_find_show_more_on_initial_ranking")
            return

        while on_screen:
            find_image_and_click(ranking_show_more_files,
                                 msg="show more",
                                 precision=precision,
                                 error_filename="fail_show_last")
            sleep_random(self.sleep_show_last / 2)
            move_mouse_close_to_center()
            sleep_random(self.sleep_show_last / 2)
            on_screen, _, _, _ = any_image_on_screen(ranking_show_more_files, precision=precision)

    def _invest_if_needed(self):
        any_zero_invest_industry = self._select_zero_investment()
        if not any_zero_invest_industry:
            return False
        self._industry_invest()
        return True

    def _select_zero_investment(self):
        invest_precision = 0.9
        ranking_invest_zero_files = get_image_paths_from_folder(RANKING_FOLDER + "/invest_zero")
        on_screen, _, _, _ = any_image_on_screen(ranking_invest_zero_files,
                                                 precision=invest_precision)
        if on_screen:
            find_image_and_click(ranking_invest_zero_files,
                                 precision=invest_precision,
                                 msg="zero investment",
                                 error_filename="fail_select_zero_investment")
            sleep_random(self.sleep_select_zero_investment)
            return True
        else:
            logging.debug("Nothing to invest, no one with zero")
            return False

    def _industry_invest(self):
        industry_invest_files = get_image_paths_from_folder(INDUSTRY_FOLDER + "/invest")
        find_image_and_click(industry_invest_files,
                             msg="invest",
                             error_filename="fail_industry_invest")
        sleep_random(self.sleep_industry_invest)
