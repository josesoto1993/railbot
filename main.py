import logging

from association.worker_bid.worker_bid import WorkerBid
from engines.pax_schedule.pax_schedule import PaxSchedule
from engines.service_engine.service_engine import ServiceEngine
from invest.city_invest.city_invest import CityInvest
from invest.industry_invest.industry_invest import IndustryInvest
from rail_utils.rail_utils import get_screenshot, sleep_random
from redeem.medals.medal_redeem import MedalRedeem

MAIN_LOOP_TIME = 60
RUN_PAX_SCHEDULE_FLAG = True
RUN_INDUSTRY_INVEST_FLAG = True
RUN_CITY_INVEST_FLAG = True
RUN_SERVICE_ENGINE_FLAG = True
RUN_WORKER_BID_FLAG = True
RUN_REDEEM_MEDAL = True


def main():
    get_screenshot(save=True)

    pax_schedule = PaxSchedule(start_minute=5)
    industry_invest = IndustryInvest()
    city_invest = CityInvest()
    service_engine = ServiceEngine()
    worker_bid = WorkerBid()
    redeem_medal = MedalRedeem()
    main_loop(pax_schedule, industry_invest, city_invest, service_engine, worker_bid, redeem_medal)


def main_loop(
        pax_schedule: PaxSchedule,
        industry_invest: IndustryInvest,
        city_invest: CityInvest,
        service_engine: ServiceEngine,
        worker_bid: WorkerBid,
        redeem_medal: MedalRedeem
):
    while True:
        _run_pax_schedule(pax_schedule)
        _run_industry_invest(industry_invest)
        _run_city_invest(city_invest)
        _run_service_engine(service_engine)
        _run_worker_bid(worker_bid)
        _run_redeem_medal(redeem_medal)

        sleep_random(MAIN_LOOP_TIME)


def _run_redeem_medal(redeem_medal: MedalRedeem):
    if RUN_REDEEM_MEDAL:
        try:
            redeem_medal.run()
        except Exception as exception:
            logging.error(str(exception))


def _run_worker_bid(worker_bid: WorkerBid):
    if RUN_WORKER_BID_FLAG:
        try:
            worker_bid.run()
        except Exception as exception:
            logging.error(str(exception))


def _run_service_engine(service_engine: ServiceEngine):
    if RUN_SERVICE_ENGINE_FLAG:
        try:
            service_engine.run()
        except Exception as exception:
            logging.error(str(exception))


def _run_city_invest(city_invest: CityInvest):
    if RUN_CITY_INVEST_FLAG:
        try:
            city_invest.run()
        except Exception as exception:
            logging.error(str(exception))


def _run_industry_invest(industry_invest: IndustryInvest):
    if RUN_INDUSTRY_INVEST_FLAG:
        try:
            industry_invest.run()
        except Exception as exception:
            logging.error(str(exception))


def _run_pax_schedule(pax_schedule: PaxSchedule):
    if RUN_PAX_SCHEDULE_FLAG:
        try:
            pax_schedule.run()
        except Exception as exception:
            logging.error(str(exception))


if __name__ == "__main__":
    main()
