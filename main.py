import logging
import time

from engines.pax_schedule.max_money import PaxSchedule
from invest.industry_invest.industry_invest import IndustryInvest
from rail_utils.rail_utils import get_screenshot

MAIN_LOOP_TIME = 60
RUN_PAX_SCHEDULE_FLAG = True
RUN_INDUSTRY_INVEST_FLAG = True

logging.basicConfig(level=logging.INFO)
# logging.root.setLevel(logging.DEBUG)


def main():
    get_screenshot(save=True)

    pax_schedule = PaxSchedule(start_minute=5)
    industry_invest = IndustryInvest()
    logging.info("Program started.")
    main_loop(pax_schedule, industry_invest)


def main_loop(pax_schedule: PaxSchedule, industry_invest: IndustryInvest):
    while True:
        if RUN_PAX_SCHEDULE_FLAG:
            run_pax_schedule(pax_schedule)
        if RUN_INDUSTRY_INVEST_FLAG:
            run_industry_invest(industry_invest)

        time.sleep(MAIN_LOOP_TIME)


def run_pax_schedule(pax_schedule: PaxSchedule):
    try:
        pax_schedule.set_schedule()
    except Exception as exception:
        logging.error(str(exception))


def run_industry_invest(industry_invest: IndustryInvest):
    try:
        industry_invest.invest()
    except Exception as exception:
        logging.error(str(exception))


if __name__ == "__main__":
    main()
