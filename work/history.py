from time import sleep
from datetime import datetime
from datetime import timedelta

from sql import get_session
from sql.models import LoginHistory
from sql.page import get_max_page
from sql.page import get_page


def init(s):
    @s.scheduled_job('cron', hour="*/1")
    def remove_login_history():
        session = get_session()
        filters = LoginHistory.creation_date < datetime.now() - timedelta(days=30)

        max_page = get_max_page(
            session=session,
            model=LoginHistory,
            filters=filters
        )

        for page in range(1, max_page + 1):
            for history in get_page(session, LoginHistory, filters, page):
                session.delete(history)

            session.commit()
            sleep(15)
