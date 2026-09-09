from sqlalchemy import create_engine 
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from .config import settings
import time
#how to implement your orm model in fastapi 
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Enable pool_pre_ping to help with dropped connections and configure engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

#creates the section factory to a specific database 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base = declarative create base class for our orm models 
Base = declarative_base()

# for fast api to connect to the database we need to create a session and close it after the request is done.
# for fastapi dependency injection we can use the yield keyword to create a session and close it after the request is done.
def get_db():
    # Create a session with a small retry loop to tolerate transient DNS/startup issues
    max_retries = 5
    delay = 1
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            db = SessionLocal()
            # quick sanity check
            db.execute(text("SELECT 1"))
            last_exc = None
            break
        except Exception as e:
            last_exc = e
            try:
                db.close()
            except Exception:
                pass
            if attempt < max_retries:
                time.sleep(delay)
                continue
            # exhausted retries
            raise

    try:
        yield db
    finally:
        db.close()#-> Automatically closes the connection when request finishes 

