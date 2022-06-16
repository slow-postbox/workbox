from os import getpid
from logging import getLogger
from logging import StreamHandler
from logging import Formatter
from logging import INFO
from logging import WARNING
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler(timezone="Asia/Seoul")
logger = getLogger()


def init_logger():
    logger.setLevel(INFO)
    handler = StreamHandler()
    handler.setFormatter(fmt=Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(hdlr=handler)
    getLogger('apscheduler.executors.default').setLevel(WARNING)


if __name__ == "__main__":
    init_logger()
    logger.info(f"workbox pid={getpid()}")

    try:
        import work
        for target in work.__all__:
            try:
                getattr(getattr(work, target), "init")(scheduler)
            except AttributeError:
                logger.critical(f"fail to init '{target}'")

        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler exited!")
