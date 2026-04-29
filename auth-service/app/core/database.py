from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# engine = the actual connection to PostgreSQL
# Think of it as the phone line to your database
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    # echo=True prints every SQL query to terminal
    # very useful for learning and debugging
)


# Session factory — creates a new session for each request
# A session is like a conversation with the database
# You open it, do your queries, then close it
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base class for all database models
# Every model (table) inherits from this
class Base(DeclarativeBase):
    pass


async def get_db():
    """
    FastAPI dependency that provides a database session.

    How it works:
    - Opens a session at the start of each request
    - Gives the session to your route/service
    - Commits (saves) everything if no errors
    - Rolls back (cancels) everything if there is an error
    - Closes the session when request is done

    yield means: "give this to the caller, wait,
    then run the cleanup code after"
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session          # give session to the route
            await session.commit() # save everything to DB
        except Exception:
            await session.rollback() # cancel everything on error
            raise
        finally:
            await session.close()  # always close the session