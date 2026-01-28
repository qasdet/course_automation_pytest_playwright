from config import db

# Получить строку подключения
connection_string = db.database_url

# Использование SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from models import Flights

engine = create_engine(db.database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Пример запроса к таблице Flights
try:
    # Получить все рейсы
    all_flights = session.query(Flights).all()
    print(f"Всего рейсов в базе: {len(all_flights)}")
    
    # Получить активные рейсы (со статусом не 'Cancelled')
    active_flights = session.query(Flights).filter(Flights.status != 'Cancelled').all()
    print(f"Активных рейсов: {len(active_flights)}")
    
    # Получить рейсы по конкретному маршруту
    route_flights = session.query(Flights).filter(Flights.route_no == 'PG0001').all()
    print(f"Рейсов по маршруту PG0001: {len(route_flights)}")
    
    # Получить рейсы с запланированным вылетом в будущем
  
    future_flights = session.query(Flights).filter(
        Flights.scheduled_departure > datetime.now()
    ).order_by(Flights.scheduled_departure).limit(10).all()
    
    print("\nБлижайшие 10 рейсов:")
    for flight in future_flights:
        print(f"Рейс {flight.flight_id}: {flight.route_no} - {flight.status}")
        print(f"  Запланирован: {flight.scheduled_departure}")
        
except Exception as e:
    print(f"Ошибка при выполнении запроса: {e}")
finally:
    session.close()