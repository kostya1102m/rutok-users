from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)