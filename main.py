from fastapi import FastAPI, Depends 
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base

from models import Doctor, Block, Diagnosis, Gender, Inspect, Patient, Place_Insp, Symptoms


engine = create_engine("postgresql://postgres:1234@localhost/new_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

metadata = MetaData()
doctor_table = Table("doctor", metadata, autoload_with=engine)

@app.get("/doctors")
def get_all_doctors():
    db = SessionLocal()
    return {"doctors": db.query(Doctor).all()}
    db.close()

@app.post("/doctors/add")
async def add_doctor(last_n: str, first_n: str, patro_n: str, phone_num: str, block_id: int, exp: int):
    db = SessionLocal()
    new_doctor = Doctor(last_n = last_n, first_n = first_n, patro_n = patro_n, phone_num = phone_num, block_id = block_id, exp = exp)
    db.add(new_doctor)
    db.commit()
    db.close()
    return{"message":"vrach dobavlen"}

@app.delete("/doctors/delete/{id}")
async def delete_doctor(id: int):
    db = SessionLocal()
    db.query(Doctor).filter(Doctor.id == id).delete()
    db.commit()
    db.close()
    return{"message":"vrach ydalen"}

@app.get("/block")
def get_all_block():
    db = SessionLocal()
    return {"block": db.query(Block).all()}
    db.close()

@app.post("/block/add")
async def add_block(address: str, block_num: int):
    db = SessionLocal()
    new_block = Block(address = address, block_num = block_num)
    db.add(new_block)
    db.commit()
    db.close()
    return{"message":"address dobavlen"}

@app.delete("/block/delete/{id}")
async def delete_block(id: int):
    db = SessionLocal()
    db.query(Block).filter(Block.id == id).delete()
    db.commit()
    db.close()
    return{"message":"address ydalen"}

@app.get("/diagnosis")
def get_all_diagnosis():
    db = SessionLocal()
    return {"diagnosis": db.query(Diagnosis).all()}
    db.close()

@app.post("/diagnosis/add")
async def add_diagnosis(diagnosis_name: str):
    db = SessionLocal()
    new_diagnosis = Diagnosis(diagnosis_name = diagnosis_name)
    db.add(new_diagnosis)
    db.commit()
    db.close()
    return{"message":"diagnos dobavlen"}

@app.delete("/diagnosis/delete/{id}")
async def diagnosis_delete(id: int):
    db = SessionLocal()
    db.query(Diagnosis).filter(Diagnosis.id == id).delete()
    db.commit()
    db.close()
    return{"message":"diagnos ydalen"}

@app.get("/inspect")
def get_all_inspect():
    db = SessionLocal()
    return {"inspect": db.query(Inspect).all()}
    db.close()

@app.post("/inspect/add")
async def add_inspect(place: int, date: date, doctor: int, patient: int, symptom_id: int, diagnosis_id: int, prescriptions: str):
    db = SessionLocal()
    new_inspect= Inspect(place = place, date = date, doctor = doctor, patient = patient, symptom_id = symptom_id, diagnosis_id = diagnosis_id, prescriptions = prescriptions)
    db.add(new_inspect)
    db.commit()
    db.close()
    return{"message":"inspect dobavlen"}

@app.delete("/inspect/delete/{id}")
async def inspect_delete(id: int):
    db = SessionLocal()
    db.query(Inspect).filter(Inspect.id == id).delete()
    db.commit()
    db.close()
    return{"message":"inspect ydalen"}

@app.get("/patient")
def get_all_patient():
    db = SessionLocal()
    return {"patient": db.query(Patient).all()}
    db.close()

@app.post("/patient/add")
async def add_patient(last_n: str, first_n: str, patro_n: str, phone_num: str, address: str, age: int, gender_char: str):
    db = SessionLocal()
    new_patient = Patient(last_n = last_n, first_n = first_n, patro_n = patro_n, phone_num = phone_num, address = address, age = age, gender_char = gender_char)
    db.add(new_patient)
    db.commit()
    db.close()
    return{"message":"patient dobavlen"}

@app.delete("/patient/delete/{id}")
async def inspect_delete(id: int):
    db = SessionLocal()
    db.query(Patient).filter(Patient.id == id).delete()
    db.commit()
    db.close()
    return{"message":"patient ydalen"}

@app.get("/place_insp")
def get_all_place_insp():
    db = SessionLocal()
    return {"place_insp": db.query(Place_Insp).all()}
    db.close()

@app.get("/symptoms")
def get_all_diagnosis():
    db = SessionLocal()
    return {"symptom": db.query(Symptoms).all()}
    db.close()

@app.post("/symptoms/add")
async def add_symptom(symptom: str):
    db = SessionLocal()
    new_symptom = Symptoms(symptom = symptom)
    db.add(new_symptom)
    db.commit()
    db.close()
    return{"message":"symptom dobavlen"}

@app.delete("/symptom/delete/{id}")
async def symptom_delete(id: int):
    db = SessionLocal()
    db.query(Symptoms).filter(Symptoms.id == id).delete()
    db.commit()
    db.close()
    return{"message":"symptom ydalen"}

