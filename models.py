from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Block(Base):
    __tablename__ = "block"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, primary_key = True)
    block_num = Column(Integer)

class Diagnosis(Base):
    __tablename__ = "diagnosis"
    id = Column(Integer, primary_key=True, index=True)
    diagnosis_name = Column(String)

class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True, index=True)
    last_n = Column(String)
    first_n = Column(String)
    patro_n = Column(String)
    phone_num = Column(String)
    block_id = Column(Integer)
    exp = Column(Integer)

class Gender(Base):
    __tablename__ = "gender"
    gender_value = Column(String)
    gender_char = Column(String, primary_key = True)
    pass

class Inspect(Base):
    __tablename__ = "inspect"
    id = Column(Integer, primary_key=True, index=True)
    place = Column(String)
    date = Column(Date)
    doctor = Column(Integer, ForeignKey("doctor.id"))
    patient = Column(Integer, ForeignKey("patient.id"))
    symptom_id = Column(String)
    diagnosis_id = Column(String)
    prescriptions = Column(String)

class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, index=True)
    last_n = Column(String)
    first_n = Column(String)
    patro_n = Column(String)
    phone_num = Column(String)
    address = Column(String, ForeignKey("block.address"))
    age = Column(Integer)
    gender_char = Column(String, ForeignKey("gender.gender_char"))

class Place_Insp(Base):
    __tablename__ = "place_insp"
    id = Column(Integer, primary_key=True, index=True)
    place = Column(String)

class Symptoms(Base):
    __tablename__ = "symptoms"
    id = Column(Integer, primary_key=True, index=True)
    symptom = Column(String)
