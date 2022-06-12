from time import sleep
from datetime import datetime
from datetime import timedelta

from sql import get_session
from sql.models import User
from sql.models import Mail
from sql.page import get_max_page
from sql.page import get_page


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
                mail_count = session.query(Mail).count()
                if mail_count == 0:
                    session.query(Mail).filter_by(
                        owner_id=user.id
                    ).delete()

                    session.delete(user)

            session.commit()
            sleep(15)
