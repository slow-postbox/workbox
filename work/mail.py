from os import environ
from time import sleep
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import and_

from sql import get_session
from sql.models import Mail
from sql.models import User
from sql.page import ITEM_PER_PAGE
from mail import sendmail


def get_page(session, model, filters, page: int) -> list:
    return session.query(model).filter(filters) \
        .offset(ITEM_PER_PAGE * (page - 1)).limit(ITEM_PER_PAGE).with_entities(
            Mail.id,
            Mail.status,
            Mail.owner_id,
            Mail.title,
        ).all()


def get_today() -> datetime:
    return datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")


def target_url(mail_id) -> str:
    if 'HOST' not in environ:
        load_dotenv()

    return environ['HOST'] + f"/mail/read/{mail_id}"


def init(s):
    @s.scheduled_job('cron', hour="*/1")
    def send_mail():
        session = get_session()
        filters = and_(
            Mail.send_date <= get_today(),
            Mail.lock == True,     # 편지가 우체통에 들어감
            Mail.status == False   # 편지가 전송된 적이 없음
        )

        page = session.query(Mail).filter(filters).limit(ITEM_PER_PAGE).all()

        for mail in page:
            user = session.query(User).with_entities(
                User.email,
            ).filter_by(
                id=mail.owner_id
            ).first()

            try:
                sendmail(
                    email=user.email,
                    url=target_url(mail_id=mail.id),
                    title=mail.title
                )

                # 메일은 전송되었음
                mail.status = True
            except Exception as e:
                print(f"FAIL TO SEND MAIL | mail_id={mail.id}")
                print(e.__str__())

            session.commit()
            sleep(3)

    # TODO: 삭제해야하는 메일 삭제 (전송했고, 읽었음)

