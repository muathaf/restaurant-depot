import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Environment Variable Extraction (Matches Docker Config)
DB_USER = os.getenv("DB_USER", "depot_admin")
DB_PASS = os.getenv("DB_PASS", "depot_password")
DB_HOST = os.getenv("DB_HOST", "localhost")  # 'mysql_db' within the Docker network
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "depot_db")

# 2. Construct MySQL Connection String using PyMySQL
# Format: mysql+pymysql://user:password@host:port/dbname
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Create the Database Core Engine
# pool_recycle helps avoid 'MySQL server has gone away' timeout errors
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

# 4. Bind Session Factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Declarative Base Mapper Class for SQLAlchemy ORM Models
Base = declarative_base()

def get_db():
    """
    Context-managed database session generator helper.
    Ensures safe opening, tracking, and absolute closing of connection pools
    after operations execute to eliminate database deadlocks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Synchronous structural schema initializer.
    Looks through all imported models inheriting from Base and automatically 
    provisions matching physical schemas inside MySQL if they do not exist.
    """
    # Imported dynamically inside standard triggers to prevent recursive dependencies
    Base.metadata.create_all(bind=engine)

