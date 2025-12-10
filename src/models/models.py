from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    Integer,
    Boolean,
    Float,
    text,
)

from config.models import bu
from config import settings


async_engine = create_async_engine(url=settings.postgres_db)
async_session = async_sessionmaker(async_engine)
async_lite_engine = create_async_engine(url="sqlite+aiosqlite:///dp.sqlite3")
async_lite_session = async_sessionmaker(async_lite_engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    # add input fields to the database
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    full_balance = mapped_column(String(101), nullable=False)
    registered: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=current_timestamp()
    )
    premium_until: Mapped[DateTime] = mapped_column(
        DateTime, nullable=True, server_default=current_timestamp()
    )
    time_zone: Mapped[str] = mapped_column(String(4))
    value: Mapped[str] = mapped_column(String(7))
    style: Mapped[str] = mapped_column(String(10))
    fiat_amount: Mapped[int] = mapped_column(
        Integer, default=bu.fiat_amount, nullable=False
    )
    crypto_amount: Mapped[int] = mapped_column(
        Integer, default=bu.crypto_amount, nullable=False
    )
    crypto_max_coins: Mapped[int] = mapped_column(
        Integer, default=bu.crypto_max_coins, nullable=False
    )

    transactions = relationship("Transaction", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"
    # add input fields to the database
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    value: Mapped[str] = mapped_column(String(7))
    amount: Mapped[str] = mapped_column(String(34))
    time: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(String(30))
    closed: Mapped[bool] = mapped_column(
        Boolean, server_default=text("FALSE"), nullable=True
    )

    user = relationship("User", back_populates="transactions")


class Payment(Base):
    __tablename__ = "payments"
    # add input fields to the database
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    transaction_uid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False)
    added: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=current_timestamp()
    )
    closed: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))

    user = relationship("User", back_populates="payments")


user_obj = User()
