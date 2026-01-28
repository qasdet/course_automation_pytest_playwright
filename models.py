from typing import List

from sqlalchemy import ARRAY, Boolean, CHAR, CheckConstraint, Column, DateTime, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, Table, Text, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB, TSTZRANGE
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped


Base = declarative_base()
metadata = Base.metadata


t_airplanes = Table(
    'airplanes', metadata,
    Column('airplane_code', CHAR(3), comment='Airplane code, IATA'),
    Column('model', Text, comment='Airplane model'),
    Column('range', Integer, comment='Maximum flight range, km'),
    Column('speed', Integer, comment='Cruise speed, km/h'),
    schema='bookings',
    comment='Airplanes'
)


class AirplanesData(Base):
    __tablename__ = 'airplanes_data'
    __table_args__ = (
        CheckConstraint('range > 0', name='airplanes_data_range_check'),
        CheckConstraint('speed > 0', name='airplanes_data_speed_check'),
        PrimaryKeyConstraint('airplane_code', name='airplanes_data_pkey'),
        {'comment': 'Airplanes (internal multilingual data)', 'schema': 'bookings'}
    )

    airplane_code = mapped_column(CHAR(3), comment='Airplane code, IATA')
    model = mapped_column(JSONB, nullable=False, comment='Airplane model')
    range = mapped_column(Integer, nullable=False, comment='Maximum flight range, km')
    speed = mapped_column(Integer, nullable=False, comment='Cruise speed, km/h')

    seats: Mapped[List['Seats']] = relationship('Seats', uselist=True, back_populates='airplanes_data')


t_airports = Table(
    'airports', metadata,
    Column('airport_code', CHAR(3), comment='Airport code, IATA'),
    Column('airport_name', Text, comment='Airport name'),
    Column('city', Text, comment='City'),
    Column('country', Text, comment='Country'),
    Column('coordinates', Text, comment='Airport coordinates (longitude and latitude)'),
    Column('timezone', Text, comment='Airport time zone'),
    schema='bookings',
    comment='Airports'
)


class AirportsData(Base):
    __tablename__ = 'airports_data'
    __table_args__ = (
        PrimaryKeyConstraint('airport_code', name='airports_data_pkey'),
        {'comment': 'Airports (internal multilingual data)', 'schema': 'bookings'}
    )

    airport_code = mapped_column(CHAR(3), comment='Airport code, IATA')
    airport_name = mapped_column(JSONB, nullable=False, comment='Airport name')
    city = mapped_column(JSONB, nullable=False, comment='City')
    country = mapped_column(JSONB, nullable=False, comment='Country')
    coordinates = mapped_column(Text, nullable=False, comment='Airport coordinates (longitude and latitude)')
    timezone = mapped_column(Text, nullable=False, comment='Airport time zone')


class Bookings(Base):
    __tablename__ = 'bookings'
    __table_args__ = (
        PrimaryKeyConstraint('book_ref', name='bookings_pkey'),
        {'comment': 'Bookings', 'schema': 'bookings'}
    )

    book_ref = mapped_column(CHAR(6), comment='Booking number')
    book_date = mapped_column(DateTime(True), nullable=False, comment='Booking date')
    total_amount = mapped_column(Numeric(10, 2), nullable=False, comment='Total booking amount')

    tickets: Mapped[List['Tickets']] = relationship('Tickets', uselist=True, back_populates='bookings')


class Flights(Base):
    __tablename__ = 'flights'
    __table_args__ = (
        CheckConstraint('actual_arrival IS NULL OR actual_departure IS NOT NULL AND actual_arrival IS NOT NULL AND actual_arrival > actual_departure', name='flight_actual_check'),
        CheckConstraint('scheduled_arrival > scheduled_departure', name='flight_scheduled_check'),
        CheckConstraint("status = ANY (ARRAY['Scheduled'::text, 'On Time'::text, 'Delayed'::text, 'Boarding'::text, 'Departed'::text, 'Arrived'::text, 'Cancelled'::text])", name='flight_status_check'),
        PrimaryKeyConstraint('flight_id', name='flights_pkey'),
        UniqueConstraint('route_no', 'scheduled_departure', name='flights_route_no_scheduled_departure_key'),
        {'comment': 'Flights', 'schema': 'bookings'}
    )

    flight_id = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), comment='Flight ID')
    route_no = mapped_column(Text, nullable=False, comment='Route number')
    status = mapped_column(Text, nullable=False, comment='Flight status')
    scheduled_departure = mapped_column(DateTime(True), nullable=False, comment='Scheduled departure time')
    scheduled_arrival = mapped_column(DateTime(True), nullable=False, comment='Scheduled arrival time')
    actual_departure = mapped_column(DateTime(True), comment='Actual departure time')
    actual_arrival = mapped_column(DateTime(True), comment='Actual arrival time')

    segments: Mapped[List['Segments']] = relationship('Segments', uselist=True, back_populates='flight')


t_timetable = Table(
    'timetable', metadata,
    Column('flight_id', Integer, comment='Flight ID'),
    Column('route_no', Text, comment='Route number'),
    Column('departure_airport', CHAR(3), comment='Airport of departure'),
    Column('arrival_airport', CHAR(3), comment='Airport of arrival'),
    Column('status', Text, comment='Flight status'),
    Column('airplane_code', CHAR(3), comment='Airplane code, IATA'),
    Column('scheduled_departure', DateTime(True), comment='Scheduled departure time'),
    Column('scheduled_departure_local', DateTime, comment="Scheduled departure time in airport's timezone"),
    Column('actual_departure', DateTime(True), comment='Actual departure time'),
    Column('actual_departure_local', DateTime, comment="Actual departure time in airport's timezone"),
    Column('scheduled_arrival', DateTime(True), comment='Scheduled arrival time'),
    Column('scheduled_arrival_local', DateTime, comment="Scheduled arrival time in airport's timezone"),
    Column('actual_arrival', DateTime(True), comment='Actual arrival time'),
    Column('actual_arrival_local', DateTime, comment="Actual arrival time in airport's timezone"),
    schema='bookings',
    comment='Detailed info about flights'
)


t_routes = Table(
    'routes', metadata,
    Column('route_no', Text, nullable=False, comment='Route number'),
    Column('validity', TSTZRANGE, nullable=False, comment='Period of validity'),
    Column('departure_airport', CHAR(3), nullable=False, comment='Airport of departure'),
    Column('arrival_airport', CHAR(3), nullable=False, comment='Airport of arrival'),
    Column('airplane_code', CHAR(3), nullable=False, comment='Airplane code, IATA'),
    Column('days_of_week', ARRAY(Integer()), nullable=False, comment='Days of week array'),
    Column('scheduled_time', Time, nullable=False, comment='Scheduled local time of departure'),
    Column('duration', INTERVAL, nullable=False, comment='Estimated duration'),
    ForeignKeyConstraint(['airplane_code'], ['bookings.airplanes_data.airplane_code'], name='routes_airplane_code_fkey'),
    ForeignKeyConstraint(['arrival_airport'], ['bookings.airports_data.airport_code'], name='routes_arrival_airport_fkey'),
    ForeignKeyConstraint(['departure_airport'], ['bookings.airports_data.airport_code'], name='routes_departure_airport_fkey'),
    Index('routes_departure_airport_lower_idx', 'departure_airport'),
    schema='bookings',
    comment='Routes'
)


class Seats(Base):
    __tablename__ = 'seats'
    __table_args__ = (
        CheckConstraint("fare_conditions = ANY (ARRAY['Economy'::text, 'Comfort'::text, 'Business'::text])", name='seat_fare_conditions_check'),
        ForeignKeyConstraint(['airplane_code'], ['bookings.airplanes_data.airplane_code'], ondelete='CASCADE', name='seats_airplane_code_fkey'),
        PrimaryKeyConstraint('airplane_code', 'seat_no', name='seats_pkey'),
        {'comment': 'Seats', 'schema': 'bookings'}
    )

    airplane_code = mapped_column(CHAR(3), nullable=False, comment='Airplane code, IATA')
    seat_no = mapped_column(Text, nullable=False, comment='Seat number')
    fare_conditions = mapped_column(Text, nullable=False, comment='Travel class')

    airplanes_data: Mapped['AirplanesData'] = relationship('AirplanesData', back_populates='seats')


class Tickets(Base):
    __tablename__ = 'tickets'
    __table_args__ = (
        ForeignKeyConstraint(['book_ref'], ['bookings.bookings.book_ref'], name='tickets_book_ref_fkey'),
        PrimaryKeyConstraint('ticket_no', name='tickets_pkey'),
        UniqueConstraint('book_ref', 'passenger_id', 'outbound', name='tickets_book_ref_passenger_id_outbound_key'),
        {'comment': 'Tickets', 'schema': 'bookings'}
    )

    ticket_no = mapped_column(Text, comment='Ticket number')
    book_ref = mapped_column(CHAR(6), nullable=False, comment='Booking number')
    passenger_id = mapped_column(Text, nullable=False, comment='Passenger ID')
    passenger_name = mapped_column(Text, nullable=False, comment='Passenger name')
    outbound = mapped_column(Boolean, nullable=False, comment='Outbound flight?')

    bookings: Mapped['Bookings'] = relationship('Bookings', back_populates='tickets')
    segments: Mapped[List['Segments']] = relationship('Segments', uselist=True, back_populates='tickets')


class Segments(Base):
    __tablename__ = 'segments'
    __table_args__ = (
        CheckConstraint("fare_conditions = ANY (ARRAY['Economy'::text, 'Comfort'::text, 'Business'::text])", name='segments_fare_conditions_check'),
        CheckConstraint('price >= 0::numeric', name='segments_price_check'),
        ForeignKeyConstraint(['flight_id'], ['bookings.flights.flight_id'], name='segments_flight_id_fkey'),
        ForeignKeyConstraint(['ticket_no'], ['bookings.tickets.ticket_no'], name='segments_ticket_no_fkey'),
        PrimaryKeyConstraint('ticket_no', 'flight_id', name='segments_pkey'),
        Index('segments_flight_id_idx', 'flight_id'),
        {'comment': 'Flight segment (leg)', 'schema': 'bookings'}
    )

    ticket_no = mapped_column(Text, nullable=False, comment='Ticket number')
    flight_id = mapped_column(Integer, nullable=False, comment='Flight ID')
    fare_conditions = mapped_column(Text, nullable=False, comment='Travel class')
    price = mapped_column(Numeric(10, 2), nullable=False, comment='Travel price')

    flight: Mapped['Flights'] = relationship('Flights', back_populates='segments')
    tickets: Mapped['Tickets'] = relationship('Tickets', back_populates='segments')


class BoardingPasses(Segments):
    __tablename__ = 'boarding_passes'
    __table_args__ = (
        ForeignKeyConstraint(['ticket_no', 'flight_id'], ['bookings.segments.ticket_no', 'bookings.segments.flight_id'], name='boarding_passes_ticket_no_flight_id_fkey'),
        PrimaryKeyConstraint('ticket_no', 'flight_id', name='boarding_passes_pkey'),
        UniqueConstraint('flight_id', 'boarding_no', name='boarding_passes_flight_id_boarding_no_key'),
        UniqueConstraint('flight_id', 'seat_no', name='boarding_passes_flight_id_seat_no_key'),
        {'comment': 'Boarding passes', 'schema': 'bookings'}
    )

    ticket_no = mapped_column(Text, nullable=False, comment='Ticket number')
    flight_id = mapped_column(Integer, nullable=False, comment='Flight ID')
    seat_no = mapped_column(Text, nullable=False, comment='Seat number')
    boarding_no = mapped_column(Integer, comment='Boarding pass number')
    boarding_time = mapped_column(DateTime(True), comment='Boarding time')
