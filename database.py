from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'postgresql://postgres:root@localhost:5432/Book_Appointment'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)




def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
        

