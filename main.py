import logging
import time

from engines.pax_schedule.max_money import PaxSchedule
from rail_utils.rail_utils import get_screenshot

MAIN_LOOP_TIME = 60

logging.basicConfig(level=logging.INFO)


def main():
    pax_schedule = PaxSchedule(start_minute=5)
    get_screenshot(save=True)
    logging.info("Program started.")
    main_loop(pax_schedule)


def main_loop(pax_schedule: PaxSchedule):
    while True:
        run_pax_schedule(pax_schedule)

        time.sleep(MAIN_LOOP_TIME)


def run_pax_schedule(pax_schedule: PaxSchedule):
    try:
        pax_schedule.set_schedule()
    except Exception as exception:
        logging.error(str(exception))


if __name__ == "__main__":
    main()
