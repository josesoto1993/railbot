import logging

from association.worker_bid.worker_bid import WorkerBid
from association.worker_bid.workers import *
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


def get_worker_data():
    return [
        (WORKER_CITY_CONNECTOR, 1_500_000),
        (WORKER_COMPETITION, 1_250_000),
        (WORKER_PAX, 3_500_000),
        (WORKER_BUILD_DISCOUNT, 3_500_000),
        (WORKER_TRACK_DISCOUNT, 3_500_000),
        (WORKER_REDUCE_WT, 1_000_000)
    ]


def main():
    get_screenshot(save=True)

    pax_schedule = PaxSchedule(start_minute=5)
    industry_invest = IndustryInvest()
    city_invest = CityInvest()
    service_engine = ServiceEngine()
    worker_bid = WorkerBid(worker_data=get_worker_data())
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
        logging.info(f"---------- Start loop ----------")
        if RUN_PAX_SCHEDULE_FLAG:
            pax_schedule.run()
        if RUN_INDUSTRY_INVEST_FLAG:
            industry_invest.run()
        if RUN_CITY_INVEST_FLAG:
            city_invest.run()
        if RUN_SERVICE_ENGINE_FLAG:
            service_engine.run()
        if RUN_WORKER_BID_FLAG:
            worker_bid.run()
        if RUN_REDEEM_MEDAL:
            redeem_medal.run()
        logging.info(f"---------- End loop ----------")

        sleep_random(MAIN_LOOP_TIME)


if __name__ == "__main__":
    main()
