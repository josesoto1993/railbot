import datetime
import logging
from typing import Optional, List

from association.worker_bid.worker_bid import WorkerBid
from engines.pax_schedule.pax_schedule import PaxSchedule
from engines.service_engine.service_engine import ServiceEngine
from invest.city_invest.city_invest import CityInvest
from invest.industry_invest.industry_invest import IndustryInvest
from rail_utils.rail_runnable import RailRunnable
from rail_utils.rail_utils import get_screenshot, sleep_random
from redeem.medals.medal_redeem import MedalRedeem

MAIN_LOOP_TIME = 60
RUN_PAX_SCHEDULE_FLAG = True
RUN_INDUSTRY_INVEST_FLAG = True
RUN_CITY_INVEST_FLAG = True
RUN_SERVICE_ENGINE_FLAG = True
RUN_WORKER_BID_FLAG = True
RUN_REDEEM_MEDAL_FLAG = True


def main():
    get_screenshot(save=True)

    tasks = []
    if RUN_PAX_SCHEDULE_FLAG:
        tasks.append(PaxSchedule(start_minute=5))
    if RUN_INDUSTRY_INVEST_FLAG:
        tasks.append(IndustryInvest())
    if RUN_CITY_INVEST_FLAG:
        tasks.append(CityInvest())
    if RUN_SERVICE_ENGINE_FLAG:
        tasks.append(ServiceEngine())
    if RUN_WORKER_BID_FLAG:
        tasks.append(WorkerBid())
    if RUN_REDEEM_MEDAL_FLAG:
        tasks.append(MedalRedeem())

    main_loop(tasks)


def main_loop(tasks: List[RailRunnable]):
    next_run_times = {task.__class__.__name__: datetime.datetime.now() for task in tasks}

    while True:
        for task in tasks:
            next_time = run_single_task(task)
            if next_time is not None:
                next_run_times[task.__class__.__name__] = next_time
        sleep_random(MAIN_LOOP_TIME)


def run_single_task(task: RailRunnable) -> Optional[datetime]:
    try:
        return task.run()
    except Exception as e:
        logging.error(str(e))
    return None


if __name__ == "__main__":
    main()
