from os import environ
from smtplib import SMTP
from email.mime.text import MIMEText

if 'SMTP_HOST' not in environ:
    from dotenv import load_dotenv
    load_dotenv()

SMTP_HOST = environ['SMTP_HOST']
SMTP_PORT = int(environ['SMTP_PORT'])
SMTP_USER = environ['SMTP_USER']
SMTP_PASSWORD = environ['SMTP_PASSWORD']


def sendmail(email: str, url: str, title: str):
    html = "\n".join([
        f"<p><a href=\"{url}\" target=\"_blank\">다음 링크</a>로 접속해 편지를 확인 해주세요.</p>",
        "<p>* 일정 시간이후 편지가 삭제되기 때문에 인쇄하기 기능을 통해 편지를 보관해주세요.</p>"
    ])

    payload = MIMEText(html, "html", "utf-8")
    payload['From'] = SMTP_USER
    payload['Subject'] = f"{environ['TITLE']} - {title}"

    with SMTP(SMTP_HOST, SMTP_PORT) as client:
        client.starttls()
        client.login(
            user=SMTP_USER,
            password=SMTP_PASSWORD
        )

        client.sendmail(
            from_addr=SMTP_USER,
            to_addrs=[email],
            msg=payload.as_string()
        )
