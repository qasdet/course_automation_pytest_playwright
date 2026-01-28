from config import db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Tickets, Bookings
import asyncio

# Получить строку подключения
connection_string = db.database_url

# Использование SQLAlchemy
database_url_async = db.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(database_url_async, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_tickets_data():
    """Асинхронная функция для получения и отображения данных билетов"""
    async with AsyncSessionLocal() as session:
        try:
            # Получить все билеты из таблицы Tickets
            result = await session.execute(select(Tickets))
            all_tickets = result.scalars().all()
            
            print(f"Всего билетов в базе: {len(all_tickets)}")
            print("=" * 100)
            
            # Вывести заголовки столбцов
            print(f"{'Номер билета':<15} {'Номер брони':<10} {'ID пассажира':<15} {'Имя пассажира':<25} {'Вылет?':<8} {'Сумма брони':<12}")
            print("-" * 100)
            
            # Вывести данные каждого билета
            for ticket in all_tickets:
                # Получить информацию о бронировании
                result = await session.execute(select(Bookings).filter(Bookings.book_ref == ticket.book_ref))
                booking = result.scalar_one_or_none()
                total_amount = booking.total_amount if booking else "N/A"
                
                # Ограничить длину отображаемых строк
                passenger_name = ticket.passenger_name[:23] if ticket.passenger_name else ""
                
                print(f"{ticket.ticket_no:<15} {ticket.book_ref:<10} {ticket.passenger_id:<15} {passenger_name:<25} "
                    f"{'Да' if ticket.outbound else 'Нет':<8} {str(total_amount):<12}")
                
            print("=" * 100)
            print(f"Выведено {len(all_tickets)} записей")
            
            # Дополнительная статистика
            print("\nСтатистика:")
            outbound_count = len([t for t in all_tickets if t.outbound])
            return_count = len([t for t in all_tickets if not t.outbound])
            print(f"- Исходящих билетов: {outbound_count}")
            print(f"- Возвращающихся билетов: {return_count}")
            
            # Топ-10 бронирований по сумме
            print("\nТоп-10 бронирований по сумме:")
            result = await session.execute(select(Bookings).order_by(Bookings.total_amount.desc()).limit(10))
            bookings_with_amount = result.scalars().all()
            print(f"{'Номер брони':<10} {'Дата':<20} {'Сумма':<12}")
            print("-" * 45)
            for booking in bookings_with_amount:
                print(f"{booking.book_ref:<10} {booking.book_date.strftime('%Y-%m-%d %H:%M'):<20} {booking.total_amount:<12}")
            
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            raise

async def main():
    """Главная асинхронная функция для запуска"""
    await get_tickets_data()

if __name__ == "__main__":
    # Запуск асинхронной функции
    asyncio.run(main())