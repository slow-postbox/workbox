from datetime import datetime
from datetime import timedelta

from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = Column(
        String(96),
        unique=True,
        nullable=False
    )

    password = Column(
        String(128),
        nullable=False
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    last_login = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    tos = Column(
        Integer,
        nullable=False,
    )

    privacy = Column(
        Integer,
        nullable=False,
    )

    admin = Column(
        Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r}>"


class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("user.id")
    )

    ip = Column(
        String(120),
        nullable=False
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    def __repr__(self):
        return f"<LoginHistory id={self.id}>"


class Code(Base):
    __tablename__ = "code"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = Column(
        String(96),
        nullable=False
    )

    # xxxx-xxxx
    code = Column(
        String(9),
        nullable=False
    )

    ip = Column(
        String(120),
        nullable=False
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    used_date = Column(
        DateTime,
        nullable=True,
        default=None
    )

    def is_used(self) -> bool:
        #   <used_date type>
        # None     : not used
        # Datetime : used
        return self.used_date is not None

    def is_expired(self) -> bool:
        return self.creation_date < datetime.now() - timedelta(minutes=3)

    def __repr__(self):
        return f"<Code id={self.id} email={self.email!r}>"


class Mail(Base):
    __tablename__ = "mail"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("user.id")
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    send_date = Column(
        DateTime,
        nullable=True,
    )

    title = Column(
        String(100),
        nullable=False
    )

    # max size = 20000
    content = Column(
        Text,
        nullable=False,
    )

    # True  =
    # False = Read, Write
    lock = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # True  = sent
    # False = not send
    status = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # True  = read
    # False = not read
    read = Column(
        Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return f"<Mail id={self.id} owner_id={self.owner_id}>"


class PasswordReset(Base):
    __tablename__ = "password_reset"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("user.id")
    )

    # 요청 생성 IP
    req_ip = Column(
        String(120),
        nullable=False
    )
    # 요청 사용 IP
    use_ip = Column(
        String(120),
        nullable=True,
        default=None
    )

    token = Column(
        String(96),
        nullable=False
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    used_date = Column(
        DateTime,
        nullable=True,
        default=None
    )

    def is_used(self) -> bool:
        #   <used_date type>
        # None     : not used
        # Datetime : used
        return self.used_date is not None

    def is_expired(self) -> bool:
        return self.creation_date < datetime.now() - timedelta(minutes=5)

    def __repr__(self):
        return f"<PasswordReset id={self.id} owner_id={self.owner_id} req_ip={self.req_ip!r}>"
