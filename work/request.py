from time import sleep
from datetime import datetime
from datetime import timedelta
from logging import getLogger

from sqlalchemy import or_

from sql import get_session
from sql.models import Code
from sql.models import PasswordReset
from sql.page import get_max_page
from sql.page import get_page

logger = getLogger()


def init(s):
    @s.scheduled_job('cron', hour="*/1")
    def remove_code():
        logger.info("removing email verify request...")
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

        logger.info("email verify request removed")
        session.close()

    @s.scheduled_job('cron', hour="*/1")
    def remove_password_reset():
        logger.info("removing password reset request...")
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

        logger.info("password reset request removed")
        session.close()
