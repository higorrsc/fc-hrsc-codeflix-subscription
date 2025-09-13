from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = "sqlite:///./subscription_service.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    """
    Create database and tables.
    """

    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Returns a database session.
    """

    with Session(engine) as session:
        yield session


__all__ = [
    "create_db_and_tables",
    "get_session",
]
