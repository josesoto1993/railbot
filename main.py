import datetime
import logging
from typing import Optional

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
    next_run_times = {}
    while True:
        next_time = _run_pax_schedule(pax_schedule)
        if next_time is not None:
            next_run_times['PaxSchedule'] = next_time

        next_time = _run_industry_invest(industry_invest)
        if next_time is not None:
            next_run_times['IndustryInvest'] = next_time

        next_time = _run_city_invest(city_invest)
        if next_time is not None:
            next_run_times['CityInvest'] = next_time

        next_time = _run_service_engine(service_engine)
        if next_time is not None:
            next_run_times['ServiceEngine'] = next_time

        next_time = _run_worker_bid(worker_bid)
        if next_time is not None:
            next_run_times['WorkerBid'] = next_time

        next_time = _run_redeem_medal(redeem_medal)
        if next_time is not None:
            next_run_times['MedalRedeem'] = next_time

        print(next_run_times)  # For debugging purposes

        sleep_random(MAIN_LOOP_TIME)


def _run_redeem_medal(runnable: MedalRedeem) -> Optional[datetime]:
    if RUN_REDEEM_MEDAL:
        return runnable.run()
    return None


def _run_worker_bid(runnable: WorkerBid) -> Optional[datetime]:
    if RUN_WORKER_BID_FLAG:
        return runnable.run()
    return None


def _run_service_engine(runnable: ServiceEngine) -> Optional[datetime]:
    if RUN_SERVICE_ENGINE_FLAG:
        return runnable.run()
    return None


def _run_city_invest(runnable: CityInvest) -> Optional[datetime]:
    if RUN_CITY_INVEST_FLAG:
        return runnable.run()
    return None


def _run_industry_invest(runnable: IndustryInvest) -> Optional[datetime]:
    if RUN_INDUSTRY_INVEST_FLAG:
        return runnable.run()
    return None


def _run_pax_schedule(runnable: PaxSchedule) -> Optional[datetime]:
    if RUN_PAX_SCHEDULE_FLAG:
        return runnable.run()
    return None


if __name__ == "__main__":
    main()
