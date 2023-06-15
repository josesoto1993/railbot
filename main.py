import logging
import time

from engines.pax_schedule.pax_schedule import PaxSchedule
from engines.service_engine.service_engine import ServiceEngine
from invest.city_invest.city_invest import CityInvest
from invest.industry_invest.industry_invest import IndustryInvest
from rail_utils.rail_utils import get_screenshot

MAIN_LOOP_TIME = 60
RUN_PAX_SCHEDULE_FLAG = True
RUN_INDUSTRY_INVEST_FLAG = True
RUN_CITY_INVEST_FLAG = True
RUN_SERVICE_ENGINE_FLAG = True

logging.basicConfig(level=logging.INFO)
# logging.root.setLevel(logging.DEBUG)


def main():
    get_screenshot(save=True)

    pax_schedule = PaxSchedule(start_minute=5)
    industry_invest = IndustryInvest()
    city_invest = CityInvest()
    service_engine = ServiceEngine()
    logging.info("Program started.")
    main_loop(pax_schedule, industry_invest, city_invest, service_engine)


def main_loop(pax_schedule: PaxSchedule, industry_invest: IndustryInvest, city_invest: CityInvest, service_engine: ServiceEngine):
    while True:
        if RUN_PAX_SCHEDULE_FLAG:
            pax_schedule.run()
        if RUN_INDUSTRY_INVEST_FLAG:
            industry_invest.run()
        if RUN_CITY_INVEST_FLAG:
            city_invest.run()
        if RUN_SERVICE_ENGINE_FLAG:
            service_engine.run()

        time.sleep(MAIN_LOOP_TIME)


if __name__ == "__main__":
    main()
