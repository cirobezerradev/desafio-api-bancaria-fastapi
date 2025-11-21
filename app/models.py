from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, String, Numeric, event, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone


STANDARD_AGENCY = "0001"


class Base(DeclarativeBase):
    pass


class AccountModel(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    holder_name: Mapped[str] = mapped_column(String(30))
    account_number: Mapped[str | None] = mapped_column(
        String(6),
        nullable=True,
        unique=True
        )
    agency_code: Mapped[str] = mapped_column(
        String(10),
        default=STANDARD_AGENCY
        )
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    transactions: Mapped[list['TransactionModel']] = relationship(
        back_populates='account',
        lazy='selectin',
        cascade='all, delete-orphan'
    )


@event.listens_for(AccountModel, 'after_insert')
def receive_after_insert(mapper, connection, target):

    new_account_number = str(target.id).zfill(6)

    stmt = (
        update(target.__table__)
        .where(target.__table__.c.id == target.id)
        .values(account_number=new_account_number)
    )

    connection.execute(stmt)
    target.account_number = new_account_number


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(15))
    value: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    account: Mapped['AccountModel'] = relationship(
        back_populates='transactions'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
