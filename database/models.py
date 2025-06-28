from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


async_engine = create_async_engine(url="sqlite+aiosqlite:///dp.sqlite3")
async_session = async_sessionmaker(async_engine)  # делаем асихронные переменные


class Base(AsyncAttrs, DeclarativeBase):
    pass


# страница юзера
class User(Base):
    __tablename__ = "users"
    # добавляем поля для ввода в базу данных
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(20), unique=True)
    full_balance = mapped_column(BigInteger, nullable=False)
    time_zone: Mapped[str] = mapped_column(String(4))
    value: Mapped[str] = mapped_column(String(7))
    style: Mapped[str] = mapped_column(String(10))
    transactions = relationship("Transaction", back_populates="user")
    fiat_amount: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    crypto_amount: Mapped[int] = mapped_column(Integer, default=8, nullable=False)


# страница транзакций
class Transaction(Base):
    __tablename__ = "transactions"
    # добавляем поля для ввода в базу данных
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.tg_id"))
    value: Mapped[str] = mapped_column(String(7))
    amount: Mapped[str] = mapped_column(String(34))
    time: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(String(30))
    user = relationship("User", back_populates="transactions")


# функция необоходимая для работы
async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
