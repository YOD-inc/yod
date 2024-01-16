# Импортирование библиотек
from fastapi import FastAPI, Depends 
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base

# Импортирование классов из файла
from models import Doctor, Block, Diagnosis, Gender, Inspect, Patient, Place_Insp, Symptoms

# Подключение к PostgreSQL
engine = create_engine("postgresql://postgres:1234@localhost/new_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание веб-приложения
app = FastAPI()

# Запросы
@app.get("/doctors", tags=["doctors"])
def get_all_doctors():
    db = SessionLocal()
    a = {"doctors": db.query(Doctor).all()}
    db.close()
    return a

@app.post("/doctors/add", tags=["doctors"])
async def add_doctor(last_n: str, first_n: str, patro_n: str, phone_num: str, block_id: int, exp: int):
    db = SessionLocal()
    new_doctor = Doctor(last_n = last_n, first_n = first_n, patro_n = patro_n, phone_num = phone_num, block_id = block_id, exp = exp)
    db.add(new_doctor)
    db.commit()
    db.close()
    return{"message":"vrach dobavlen"}

@app.delete("/doctors/delete/{id}", tags=["doctors"])
async def delete_doctor(id: int):
    db = SessionLocal()
    db.query(Doctor).filter(Doctor.id == id).delete()
    db.commit()
    db.close()
    return{"message":"vrach ydalen"}

@app.get("/block", tags=["block"])
def get_all_block():
    db = SessionLocal()
    a =  {"block": db.query(Block).all()}
    db.close()
    return a

@app.post("/block/add", tags=["block"])
async def add_block(address: str, block_num: int):
    db = SessionLocal()
    new_block = Block(address = address, block_num = block_num)
    db.add(new_block)
    db.commit()
    db.close()
    return{"message":"address dobavlen"}

@app.delete("/block/delete/{id}", tags=["block"])
async def delete_block(id: int):
    db = SessionLocal()
    db.query(Block).filter(Block.id == id).delete()
    db.commit()
    db.close()
    return{"message":"address ydalen"}

@app.get("/diagnosis", tags=["diagnosis"])
def get_all_diagnosis():
    db = SessionLocal()
    a =  {"diagnosis": db.query(Diagnosis).all()}
    db.close()
    return a

@app.post("/diagnosis/add", tags=["diagnosis"])
async def add_diagnosis(diagnosis_name: str):
    db = SessionLocal()
    new_diagnosis = Diagnosis(diagnosis_name = diagnosis_name)
    db.add(new_diagnosis)
    db.commit()
    db.close()
    return{"message":"diagnos dobavlen"}

@app.delete("/diagnosis/delete/{id}", tags=["diagnosis"])
async def diagnosis_delete(id: int):
    db = SessionLocal()
    db.query(Diagnosis).filter(Diagnosis.id == id).delete()
    db.commit()
    db.close()
    return{"message":"diagnos ydalen"}

@app.get("/gender", tags=["gender"])
def get_all_diagnosis():
    db = SessionLocal()
    a =  {"gender": db.query(Gender).all()}
    db.close()
    return a

@app.get("/inspect", tags=["inspect"])
def get_all_inspect():
    db = SessionLocal()
    a = {"inspect": db.query(Inspect).all()}
    db.close()
    return a

@app.post("/inspect/add", tags=["inspect"])
async def add_inspect(place: int, date: date, doctor: int, patient: int, symptom_id: int, diagnosis_id: int, prescriptions: str):
    db = SessionLocal()
    new_inspect= Inspect(place = place, date = date, doctor = doctor, patient = patient, symptom_id = symptom_id, diagnosis_id = diagnosis_id, prescriptions = prescriptions)
    db.add(new_inspect)
    db.commit()
    db.close()
    return{"message":"inspect dobavlen"}

@app.delete("/inspect/delete/{id}", tags=["inspect"])
async def inspect_delete(id: int):
    db = SessionLocal()
    db.query(Inspect).filter(Inspect.id == id).delete()
    db.commit()
    db.close()
    return{"message":"inspect ydalen"}

@app.get("/patient", tags=["patient"])
def get_all_patient():
    db = SessionLocal()
    a = {"patient": db.query(Patient).all()}
    db.close()
    return a

@app.post("/patient/add", tags=["patient"])
async def add_patient(last_n: str, first_n: str, patro_n: str, phone_num: str, address: str, age: int, gender_char: str):
    db = SessionLocal()
    new_patient = Patient(last_n = last_n, first_n = first_n, patro_n = patro_n, phone_num = phone_num, address = address, age = age, gender_char = gender_char)
    db.add(new_patient)
    db.commit()
    db.close()
    return{"message":"patient dobavlen"}

@app.delete("/patient/delete/{id}", tags=["patient"])
async def inspect_delete(id: int):
    db = SessionLocal()
    db.query(Patient).filter(Patient.id == id).delete()
    db.commit()
    db.close()
    return{"message":"patient ydalen"}

@app.get("/place_insp", tags=["place_insp"])
def get_all_place_insp():
    db = SessionLocal()
    a = {"place_insp": db.query(Place_Insp).all()}
    db.close()
    return a

@app.get("/symptoms", tags=["symptoms"])
def get_all_diagnosis():
    db = SessionLocal()
    a = {"symptom": db.query(Symptoms).all()}
    db.close()
    return a

@app.post("/symptoms/add", tags=["symptoms"])
async def add_symptom(symptom: str):
    db = SessionLocal()
    new_symptom = Symptoms(symptom = symptom)
    db.add(new_symptom)
    db.commit()
    db.close()
    return{"message":"symptom dobavlen"}

@app.delete("/symptom/delete/{id}", tags=["symptoms"])
async def symptom_delete(id: int):
    db = SessionLocal()
    db.query(Symptoms).filter(Symptoms.id == id).delete()
    db.commit()
    db.close()
    return{"message":"symptom ydalen"}