from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy base model
Base = declarative_base()


# Database model for storing names
class NameEntry(Base):
    __tablename__ = "names"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


# Database setup
DATABASE_URL = "sqlite:///./names.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)
