from apscheduler.schedulers.blocking import BlockingScheduler
from main import *
import logging
from datetime import datetime


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    downloader = Downloader()
    analyser = Analyser()
    scheduler = BlockingScheduler(logger=logger)
    scheduler.add_job(downloader.run, 'interval', seconds=30, next_run_time=datetime.now())
    scheduler.add_job(analyser.run, 'interval', seconds=30, next_run_time=datetime.now())

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

