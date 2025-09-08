from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Integer, Boolean, DATETIME
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from datetime import datetime, timezone


async_engine = create_async_engine(url="sqlite+aiosqlite:///dp.sqlite3")
async_session = async_sessionmaker(async_engine)  # делаем асихронные переменные


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    # add input fields to the database
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(20), unique=True)
    full_balance = mapped_column(BigInteger, nullable=False)
    registered: Mapped[DateTime] = mapped_column(
        DATETIME, nullable=False, default=datetime.now(timezone.utc)
    )
    premium_until: Mapped[DateTime] = mapped_column(
        DATETIME, nullable=True, default=datetime.now(timezone.utc)
    )
    time_zone: Mapped[str] = mapped_column(String(4))
    value: Mapped[str] = mapped_column(String(7))
    style: Mapped[str] = mapped_column(String(10))
    fiat_amount: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    crypto_amount: Mapped[int] = mapped_column(Integer, default=8, nullable=False)
    crypto_max_coins: Mapped[int] = mapped_column(Integer, default=16, nullable=False)

    transactions = relationship("Transaction", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"
    # add input fields to the database
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.tg_id"))
    value: Mapped[str] = mapped_column(String(7))
    amount: Mapped[str] = mapped_column(String(34))
    time: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(String(30))

    user = relationship("User", back_populates="transactions")


class Payment(Base):
    __tablename__ = "payments"
    # add input fields to the database
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.tg_id"))
    transaction_uid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False)
    added: Mapped[DateTime] = mapped_column(DATETIME, nullable=False, default=datetime.now(timezone.utc))
    closed: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="payments")


# function needed for work
async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
