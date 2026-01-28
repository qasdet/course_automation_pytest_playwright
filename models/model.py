import datetime

from models import model
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Flights(Base):
    __tablename__ = "flights"

    flight_id: Mapped[int] = mapped_column(primary_key=True)
    route_no: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    scheduled_departure: Mapped[datetime] = mapped_column()
    scheduled_arrival: Mapped[datetime] = mapped_column()
    actual_departure: Mapped[datetime] = mapped_column()
    actual_arrival: Mapped[datetime] = mapped_column()
