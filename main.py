import logging

from association.worker_bid.worker_bid import WorkerBid
from engines.pax_schedule.pax_schedule import PaxSchedule
from engines.service_engine.service_engine import ServiceEngine
from invest.city_invest.city_invest import CityInvest
from invest.industry_invest.industry_invest import IndustryInvest
from rail_utils.main_loop_handler import MainLoopHandler
from rail_utils.rail_utils import get_screenshot
from redeem.medals.medal_redeem import MedalRedeem

START_PAX_SCHEDULE_MINUTE = 0
RUN_PAX_SCHEDULE_FLAG = True
RUN_INDUSTRY_INVEST_FLAG = True
RUN_CITY_INVEST_FLAG = True
RUN_SERVICE_ENGINE_FLAG = True
RUN_WORKER_BID_FLAG = True
RUN_REDEEM_MEDAL_FLAG = True
RUN_BUILDING_BONUS_FLAG = False
BEEP_COUNTDOWN_FLAG = False

logging.root.setLevel(logging.INFO)


def main():
    get_screenshot(save=True)

    # TODO: sonar beep al iniciar si la carpeta errors tiene algun archivo

    tasks = []
    if RUN_PAX_SCHEDULE_FLAG:
        tasks.append(PaxSchedule(start_minute=START_PAX_SCHEDULE_MINUTE))
    if RUN_INDUSTRY_INVEST_FLAG:
        tasks.append(IndustryInvest())
    if RUN_CITY_INVEST_FLAG:
        tasks.append(CityInvest())
    if RUN_SERVICE_ENGINE_FLAG:
        tasks.append(ServiceEngine())
    if RUN_WORKER_BID_FLAG:
        tasks.append(WorkerBid())
        # TODO: que se chequeen TODOS los workers, y tener una lista de los que interesan o algo
    if RUN_REDEEM_MEDAL_FLAG:
        tasks.append(MedalRedeem())
    if RUN_BUILDING_BONUS_FLAG:
        logging.info("Cant run BuildingBonus as is disabled")
        # tasks.append(BuildingBonus())

    loop = MainLoopHandler(tasks, enable_count_down=BEEP_COUNTDOWN_FLAG)
    loop.run()


if __name__ == "__main__":
    main()
