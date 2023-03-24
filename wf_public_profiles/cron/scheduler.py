from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import dateutil.tz

from wf_public_profiles.log import logger
from wf_public_profiles.db.session import SessionLocal

from ..tasks import tasks


class Scheduler:
    def __init__(self):
        self.db = SessionLocal()

        self.scheduler = BlockingScheduler()

        cron_trigger = CronTrigger(
            hour="*",  # Execute every hour
        )
        self.scheduler.add_job(
            tasks.update_public_profiles,
            id="update_public_profiles",
            trigger=cron_trigger,
            replace_existing=True,
            coalesce=True,
            next_run_time=datetime.now(dateutil.tz.tzutc()),
            misfire_grace_time=2,
            kwargs={"db": self.db},
        )

    def start(self):
        logger.info("Starting background scheduler")
        self.scheduler.start()

    def __del__(self):
        if self.db:
            self.db.close()
