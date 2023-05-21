import datetime
import logging
import random
import time

from engines.pax_schedule import max_money as pax_schedule_max_money
from rail_utils.rail_utils import get_screenshot

logging.basicConfig(level=logging.INFO)


def main():
    get_screenshot(save=True)
    print("Program started.")
    main_loop()


def main_loop():
    while True:
        try:
            run_pax_schedule()
            target_time = get_next_target_time()
            sleep_till_target_time(target_time)
        except Exception as exception:
            logging.error(str(exception))


def run_pax_schedule():
    pax_schedule_max_money.set_schedule()


def get_next_target_time():
    current_datetime = datetime.datetime.now()
    target_hour = (current_datetime.hour + 1) % 24
    target_minute = random.randint(35, 45)
    target_datetime = current_datetime.replace(hour=target_hour, minute=target_minute)

    if target_datetime < current_datetime:
        target_datetime += datetime.timedelta(days=1)

    print(f"Next run at {target_datetime.time()}")

    return target_datetime


def sleep_till_target_time(target_time):
    remaining_time = target_time - datetime.datetime.now()
    remaining_seconds = remaining_time.total_seconds()
    print(f"Sleeping {remaining_seconds}'")
    time.sleep(remaining_seconds)
    print(f"----- Run Start -----")


if __name__ == "__main__":
    main()
