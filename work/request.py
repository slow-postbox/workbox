from time import sleep
from datetime import datetime
from datetime import timedelta

from sqlalchemy import or_

from sql import get_session
from sql.models import Code
from sql.models import PasswordReset
from sql.page import get_max_page
from sql.page import get_page


def init(s):
    @s.scheduled_job('cron', hour="*/1")
    def remove_code():
        session = get_session()
        filters = or_(
            Code.used_date != None,
            Code.creation_date < datetime.now() - timedelta(minutes=3)
        )

        max_page = get_max_page(
            session=session,
            model=Code,
            filters=filters
        )

        for page in range(1, max_page + 1):
            for code in get_page(session, Code, filters, page):
                session.delete(code)

            session.commit()
            sleep(15)

    @s.scheduled_job('cron', hour="*/1")
    def remove_password_reset():
        session = get_session()
        filters = or_(
            PasswordReset.used_date != None,
            PasswordReset.creation_date < datetime.now() - timedelta(minutes=5)
        )

        max_page = get_max_page(
            session=session,
            model=PasswordReset,
            filters=filters
        )

        for page in range(1, max_page + 1):
            for password_reset in get_page(session, PasswordReset, filters, page):
                session.delete(password_reset)

            session.commit()
            sleep(15)
