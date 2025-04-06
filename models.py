from unittest.mock import Base
from sqlalchemy.dialects.mysql import TEXT,JSON,BOOLEAN, DATETIME,INTEGER
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
        
class Patients(Base):
    __tablename__ = 'patients_details'
    
    id:Mapped[INTEGER] = mapped_column(INTEGER,primary_key=True,index = True,autoincrement=True)
    first_name:Mapped[TEXT] = mapped_column(TEXT)
    last_name:Mapped[TEXT] = mapped_column(TEXT)
    age:Mapped[INTEGER] = mapped_column(INTEGER)
    gender: Mapped[TEXT] = mapped_column(TEXT)
    phone:Mapped[INTEGER] = mapped_column(INTEGER)
    guardian_name:Mapped[TEXT] = mapped_column(TEXT)
    pincode: Mapped[INTEGER] = mapped_column(INTEGER)
    
class Doctors(Base):
    __tablename__ = 'doctors'
    
    id:Mapped[INTEGER] = mapped_column(INTEGER,primary_key=True,index = True,autoincrement=True)
    name:Mapped[TEXT] = mapped_column(TEXT)
    locations:Mapped[ARRAY[TEXT]]= mapped_column(ARRAY(TEXT))
    