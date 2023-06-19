import datetime
import logging

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
        logging.info(f"----- Run industry invest: Start at {datetime.datetime.now()} -----")
        open_tab(Tabs.RANKINGS)
        self._select_subtab_industries()
        self._select_subsubtab_invest()
        self._show_last()
        any_zero_invest_industry = self._select_zero_investment()
        if not any_zero_invest_industry:
            return False
        self._industry_invest()
        return True

    def _update_next_run_time(self, invest_done=True):
        if invest_done:
            logging.info(f"----- May have more industries to invest, next loop invest another one -----")
        else:
            target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

            self.next_run_time = target_datetime
            logging.info(f"----- Next industry invest at {target_datetime.time()} -----")

    def _select_subtab_industries(self):
        find_image_and_click([RANKING_SUBTAB_INDUSTRIES], msg="subtab industries")
        sleep_random(self.sleep_select_subtab_industries)

    def _select_subsubtab_invest(self):
        find_image_and_click([RANKING_SUBSUBTAB_INVEST], msg="subsubtab invest")
        sleep_random(self.sleep_select_subsubtab_invest)

    def _show_last(self):
        on_screen = True
        while on_screen:
            find_image_and_click([RANKING_SHOW_MORE], msg="show more")
            sleep_random(self.sleep_show_last / 2)
            move_mouse_close_to_center()
            sleep_random(self.sleep_show_last / 2)
            on_screen, position, _ = image_on_screen(RANKING_SHOW_MORE, precision=0.9)

    def _select_zero_investment(self):
        on_screen, position, _ = image_on_screen(RANKING_SUBSUBTAB_INVEST_ZERO, precision=0.95)
        if on_screen:
            find_image_and_click([RANKING_SUBSUBTAB_INVEST_ZERO], msg="zero investment")
            sleep_random(self.sleep_select_zero_investment)
            return True
        else:
            logging.debug("Nothing to invest, no one with zero")
            return False

    def _industry_invest(self):
        find_image_and_click([INDUSTRY_INVEST_BASE, INDUSTRY_INVEST_VOUCHER_BASE], msg="invest")
        sleep_random(self.sleep_industry_invest)
