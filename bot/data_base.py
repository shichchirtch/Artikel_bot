import fake_useragent
from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

session_marker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

class User(Base):

    __tablename__ = 'users'
    index: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tg_us_id: Mapped[int] = mapped_column(BigInteger) # tg user id
    user_name: Mapped[str] = mapped_column(String(200), nullable=False)
    der: Mapped[str] = mapped_column(String, default='DER\n\n', nullable=True)
    die: Mapped[str] = mapped_column(String, default='DIE\n\n', nullable=True)
    das: Mapped[str] = mapped_column(String, default='DAS\n\n', nullable=True)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


user = fake_useragent.UserAgent().random

# header = {'user-agent':user}
site_url = 'https://der-artikel.de/'

site_headers = {
    'Accept': '*/*',
    'User-Agent': user}