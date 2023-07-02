import datetime
import logging
from typing import Optional

from rail_utils.rail_utils import find_image_and_click, sleep_random, move_mouse_close_to_center, any_image_on_screen
from rail_utils.tabs_enum import Tabs
from rail_utils.tabs_util import open_tab

INVEST_MINUTES_TO_RECHECK = 180

RANKING_FOLDER = "data/tab_ranking"
RANKING_SUBTAB_INDUSTRIES = RANKING_FOLDER + "/ranking_subtab_industries_base.png"
RANKING_SUBTAB_INDUSTRIES_SMALL = RANKING_FOLDER + "/ranking_subtab_industries_base_small.png"
RANKING_SUBSUBTAB_INVEST = RANKING_FOLDER + "/ranking_subtab_industries_invest_base.png"
RANKING_SUBSUBTAB_INVEST_SMALL = RANKING_FOLDER + "/ranking_subtab_industries_invest_base_small.png"
RANKING_SHOW_MORE = RANKING_FOLDER + "/ranking_subtab_industries_show_more_base.png"
RANKING_SHOW_MORE_SMALL = RANKING_FOLDER + "/ranking_subtab_industries_show_more_base_small.png"
RANKING_SUBSUBTAB_INVEST_ZERO = RANKING_FOLDER + "/ranking_subtab_industries_invest_zero_base.png"
RANKING_SUBSUBTAB_INVEST_ZERO_SMALL = RANKING_FOLDER + "/ranking_subtab_industries_invest_zero_base_small.png"

INDUSTRY_FOLDER = "data/industry"
INDUSTRY_INVEST_BASE = INDUSTRY_FOLDER + "/industry_invest_base.png"
INDUSTRY_INVEST_BASE_SMALL = INDUSTRY_FOLDER + "/industry_invest_base_small.png"
INDUSTRY_INVEST_VOUCHER_BASE = INDUSTRY_FOLDER + "/industry_invest_voucher_base.png"
INDUSTRY_INVEST_VOUCHER_BASE_SMALL = INDUSTRY_FOLDER + "/industry_invest_voucher_base_small.png"

logging.basicConfig(level=logging.INFO)


class IndustryInvest:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()
        self.sleep_select_subtab_industries = 5
        self.sleep_select_subsubtab_invest = 10
        self.sleep_show_last = 2
        self.sleep_select_zero_investment = 5
        self.sleep_industry_invest = 5

    def run(self) -> Optional[datetime]:
        try:
            if self._should_run():
                invest_done = self._run_invest()
                self._update_next_run_time(invest_done)
            return self.next_run_time
        except Exception as exception:
            logging.error(str(exception))
            return None

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_invest(self):
        logging.info(f"----- Run industry invest: Start at {datetime.datetime.now().time()} -----")
        open_tab(Tabs.RANKINGS.value)
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
            logging.info("----- May have more industries to invest, next loop invest another one -----")
        else:
            target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=INVEST_MINUTES_TO_RECHECK)

            self.next_run_time = target_datetime
            logging.info(f"----- Next industry invest at {target_datetime.time()} -----")

    def _select_subtab_industries(self):
        subtab_industries = [RANKING_SUBTAB_INDUSTRIES, RANKING_SUBTAB_INDUSTRIES_SMALL]
        find_image_and_click(subtab_industries, msg="subtab industries")
        sleep_random(self.sleep_select_subtab_industries)

    def _select_subsubtab_invest(self):
        subsubtab_invest = [RANKING_SUBSUBTAB_INVEST, RANKING_SUBSUBTAB_INVEST_SMALL]
        find_image_and_click(subsubtab_invest, msg="subsubtab invest")
        sleep_random(self.sleep_select_subsubtab_invest)

    def _show_last(self):
        show_more_btn = [RANKING_SHOW_MORE, RANKING_SHOW_MORE_SMALL]
        on_screen = True
        while on_screen:
            find_image_and_click(show_more_btn, msg="show more", precision=0.9)
            sleep_random(self.sleep_show_last / 2)
            move_mouse_close_to_center()
            sleep_random(self.sleep_show_last / 2)
            on_screen, _, _, _ = any_image_on_screen(show_more_btn, precision=0.9)

    def _select_zero_investment(self):
        invest_zero_label = [RANKING_SUBSUBTAB_INVEST_ZERO, RANKING_SUBSUBTAB_INVEST_ZERO_SMALL]
        on_screen, _, _, _ = any_image_on_screen(invest_zero_label, precision=0.95)
        if on_screen:
            find_image_and_click(invest_zero_label, msg="zero investment")
            sleep_random(self.sleep_select_zero_investment)
            return True
        else:
            logging.debug("Nothing to invest, no one with zero")
            return False

    def _industry_invest(self):
        invest_label = [INDUSTRY_INVEST_BASE,
                        INDUSTRY_INVEST_BASE_SMALL,
                        INDUSTRY_INVEST_VOUCHER_BASE,
                        INDUSTRY_INVEST_VOUCHER_BASE_SMALL]
        find_image_and_click(invest_label, msg="invest")
        sleep_random(self.sleep_industry_invest)
