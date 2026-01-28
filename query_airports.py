import asyncio
from config import db
from sqlalchemy.ext.asyncio import create_async_engine, 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import AirportsData

# Использование асинхронного SQLAlchemy
# Преобразуем URL для асинхронного подключения (postgresql -> postgresql+asyncpg)
database_url_async = db.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(database_url_async, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_airports_data():
    """Асинхронная функция для получения и отображения данных аэропортов"""
    async with AsyncSessionLocal() as session:
        try:
            # Асинхронный запрос к таблице AirportsData
            stmt = select(AirportsData)
            result = await session.execute(stmt)
            all_airports = result.scalars().all()
            
            print(f"Всего аэропортов в базе: {len(all_airports)}")
            print("=" * 80)
            
            # Вывести заголовки столбцов
            print(f"{'Код':<8} {'Название':<30} {'Город':<20} {'Страна':<15} {'Часовой пояс':<20}")
            print("-" * 80)
            
            # Вывести данные каждого аэропорта
            for airport in all_airports:
                # Извлекаем значения из JSONB полей
                airport_name = airport.airport_name.get('ru', airport.airport_name.get('en', '')) if isinstance(
                    airport.airport_name, dict) else str(airport.airport_name)
                city = airport.city.get('ru', airport.city.get('en', '')) if isinstance(airport.city, dict) else str(
                    airport.city)
                country = airport.country.get('ru', airport.country.get('en', '')) if isinstance(airport.country,
                                                                                                 dict) else str(airport.country)
                
                print(
                    f"{airport.airport_code:<8} {airport_name[:28]:<30} {city[:18]:<20} {country[:13]:<15} {airport.timezone:<20}")
                
            print("=" * 80)
            print(f"Выведено {len(all_airports)} записей")
            
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(get_airports_data())