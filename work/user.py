from time import sleep
from datetime import datetime
from datetime import timedelta
from hashlib import md5
from logging import getLogger

from sql import get_session
from sql.models import User
from sql.models import LoginHistory
from sql.models import PasswordReset
from sql.models import Code
from sql.models import Mail
from sql.models import UserLock
from sql.page import get_max_page
from sql.page import get_page

logger = getLogger()


def init(s):
    @s.scheduled_job('cron', day="*/1")
    def old_user():
        session = get_session()
        filters = User.last_login < datetime.now() - timedelta(days=365)

        max_page = get_max_page(
            session=session,
            model=User,
            filters=filters
        )

        for page in range(1, max_page + 1):
            for user in get_page(session, User, filters, page):
                if user.admin is False:
                    if session.query(UserLock).filter_by(
                        owner_id=user.id
                    ).count() == 0 and session.query(Mail).filter_by(
                        owner_id=user.id
                    ).count() == 0:
                        session.query(LoginHistory).filter_by(
                            owner_id=user.id
                        ).delete()
                        session.query(Code).filter_by(
                            owner_id=user.id
                        ).delete()
                        session.query(PasswordReset).filter_by(
                            owner_id=user.id
                        ).delete()

                        session.delete(user)
                        logger.info(f"user deleted / {user.id} : {md5(user.email.encode()).hexdigest()}")

            session.commit()
            sleep(15)

        session.close()
