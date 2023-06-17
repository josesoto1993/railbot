import datetime
import logging

WORKER_BID_MINUTES_TO_RECHECK = 45


class WorkerBid:
    def __init__(self):
        self.next_run_time = datetime.datetime.now()

    def run(self):
        if self._should_run():
            try:
                self._run_worker_bid()
                self._update_next_run_time()
            except Exception as exception:
                logging.error(str(exception))
                return

    def _should_run(self):
        return datetime.datetime.now() >= self.next_run_time

    def _run_worker_bid(self):
        logging.info(f"----- Run worker bid: Start at {datetime.datetime.now()} -----")

        self._update_next_run_time()
        raise Exception(f"Implement: _run_worker_bid")

    def _update_next_run_time(self):
        target_datetime = datetime.datetime.now() + datetime.timedelta(minutes=WORKER_BID_MINUTES_TO_RECHECK)

        self.next_run_time = target_datetime
        logging.info(f"----- Next worker bid check at {target_datetime.time()} -----")
