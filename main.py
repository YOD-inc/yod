# Импортирование библиотек
from fastapi import FastAPI, Depends, HTTPException 
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, literal_column, join


# Импортирование классов из файла
from models import Doctor, Block, Diagnosis, Gender, Inspect, Patient, Place_Insp, Symptoms, User, UserCreate


# Подключение к PostgreSQL
engine = create_engine("postgresql://postgres:1234@localhost/new_db")
# engine = create_engine("postgresql://postgres:admin@localhost/test_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Создание веб-приложения
app = FastAPI()


# Подключение CORS механизма
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# def get_db():
#     db = SessionLocal()
#     try: 
#         yield db
#     finally:
#         db.close()


# Запросы

# @app.post("/users", tags=["Users"])
# async def get_user(last_name: str, first_name: str, password : str, user_name: str):
#     db = SessionLocal()
#     new_user = db.query(User(last_name = last_name, first_name = first_name, password = password, user_name = user_name)).filter(User.user_name == User.user_name).first()
#     if new_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     # if db.query(User).filter(User.user_name == user_name) == True:
#     #     return{"message":"smenite imya usera"}
#     new_user = User(user_name=User.user_name)
#     db.add(new_user)
#     db.commit()
#     db.close()
#     return{"message":"user dobavlen"}


# Для пользователей

@app.post("/users/reg", tags=["Users"])
async def get_user(last_name: str, first_name: str, password: str, user_name: str):
    db = SessionLocal()
    new_user = db.query(User).filter(user_name == User.user_name).first()
    if new_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already taken")
    # if db.query(User).filter(User.user_name == user_name) == True:
    #     return{"message":"smenite imya usera"}
    else:
        new_user = User(last_name = last_name, first_name = first_name, password = password, user_name = user_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return{"message":"User dobavlen"}

@app.post("/users/log", tags=["Users"])
async def get_user(user_name: str, password: str):
    db = SessionLocal()
    check_user = User(user_name = user_name, password = password)
    check = db.query(User).filter(User.user_name == user_name).first()
    if check:
        # check_pass = db.query(User).filter(User.user_name == password)
        if check_user.password == check.password:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=400, detail="Invalid username or password")
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    pass


# Для врачей

# @app.get("/doctors", tags=["doctors"])
# def get_all_doctors():
#     db = SessionLocal()
#     a = {"doctor": db.query(Doctor).all()}
#     db.close()
#     return a

@app.get("/doctors", tags=["doctors"])
def get_all_doctors():
    db = SessionLocal()
    a = {"inspect_choice_doctor": db.query(
        select([
            Doctor.c.id,
            (Doctor.c.last_n + ' ' + Doctor.c.first_n + ' ' + Doctor.c.patro_n).label('full_n'),
            Doctor.c.phone_num,
            Doctor.c.block_id,
            Doctor.c.exp
        ])
        .select_from(Doctor)
    )}
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


# Для участков

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


# Для диагнозов

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


# Для пола

@app.get("/gender", tags=["gender"])
def get_all_diagnosis():
    db = SessionLocal()
    a =  {"gender": db.query(Gender).all()}
    db.close()
    return a


# Для осмотров

@app.get("/inspect", tags=["inspect"])
def get_all_inspect():
    db = SessionLocal()
    a = {"inspect": db.query(Inspect).all()}
    db.close()
    return a

@app.post("/inspect/add", tags=["inspect"])
async def add_inspect(place: int, date: date, doctor: int, patient: int, symptom_id: int, diagnosis_id: int, prescriptions: str):
    db = SessionLocal()
    new_inspect = Inspect(place = place, date = date, doctor = doctor, patient = patient, symptom_id = symptom_id, diagnosis_id = diagnosis_id, prescriptions = prescriptions)
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

@app.get("/inspect/choice_place", tags=["inspect choices"])
def inspect_choice():
    db = SessionLocal()
    a = {"inspect_choice_place": db.query(
        select([
            Place_Insp.c.place,
        ])
        .select_from(Place_Insp)
    )}
    db.close()
    return a

@app.get("/inspect/choice_doctor", tags=["inspect choices"])
def doctor_choice():
    db = SessionLocal()
    a = {"inspect_choice_doctor": db.query(
        select([
            (Doctor.c.last_n + ' ' + Doctor.c.first_n + ' ' + Doctor.c.patro_n).label('doctor_full_n')
        ])
        .select_from(Doctor)
    )}
    db.close()
    return a

@app.get("/inspect/choice_patient", tags=["inspect choices"])
def patient_choice():
    db = SessionLocal()
    a = {"inspect_choice_patient": db.query(
        select([
            (Patient.c.last_n + ' ' + Patient.c.first_n + ' ' + Patient.c.patro_n).label('patient_full_n')
        ])
        .select_from(Patient)
    )}
    db.close()
    return a

@app.get("/inspect/choice_symptom", tags=["inspect choices"])
def symptom_choice():
    db = SessionLocal()
    a = {"inspect_choice_symptom": db.query(
        select([
            Symptoms.c.symptom,
        ])
        .select_from(Symptoms)
    )}
    db.close()
    return a

@app.get("/inspect/choice_diagnosis", tags=["inspect choices"])
def diagnosis_choice():
    db = SessionLocal()
    a = {"inspect_choice_diagnosis": db.query(
        select([
            Diagnosis.c.diagnosis_name,
        ])
        .select_from(Diagnosis)
    )}
    db.close()
    return a


# Для пациентов

@app.get("/patients", tags=["patient"])
def get_all_patient():
    db = SessionLocal()
    a = {"patient": db.query(Patient).all()}
    db.close()
    return a

@app.post("/patients/add", tags=["patient"])
async def add_patient(last_n: str, first_n: str, patro_n: str, phone_num: str, address: str, age: int, gender_char: str):
    db = SessionLocal()
    new_patient = Patient(last_n = last_n, first_n = first_n, patro_n = patro_n, phone_num = phone_num, address = address, age = age, gender_char = gender_char)
    db.add(new_patient)
    db.commit()
    db.close()
    return{"message":"patient dobavlen"}

@app.delete("/patients/delete/{id}", tags=["patient"])
async def inspect_delete(id: int):
    db = SessionLocal()
    db.query(Patient).filter(Patient.id == id).delete()
    db.commit()
    db.close()
    return{"message":"patient ydalen"}


# Для мест осмотра

@app.get("/place_insp", tags=["place_insp"])
def get_all_place_insp():
    db = SessionLocal()
    a = {"place_insp": db.query(Place_Insp).all()}
    db.close()
    return a


# Для симптомов

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

@app.delete("/symptoms/delete/{id}", tags=["symptoms"])
async def symptom_delete(id: int):
    db = SessionLocal()
    db.query(Symptoms).filter(Symptoms.id == id).delete()
    db.commit()
    db.close()
    return{"message":"symptom ydalen"}



# @app.get("/test_users", tags=["test_users"])
# def get_all_test_users():
#     db = SessionLocal()
#     a = {"test_users": db.query(Test_User).all()}
#     db.close()
#     return a

# @app.post("/test_users/add", tags=["test_users"])
# def post_data(user_input: UserInput):
#     test_user = Test_User(**user_input.dict())

#     db = SessionLocal()
#     db.add(test_user)
#     db.commit()
#     db.refresh(test_user)
#     db.close()

#     return {"message": "Data received and stored successfully", "data": user_input.dict()}
   
# @app.delete("/test_users/delete/{id}", tags=["test_users"])
# def delete_user(test_user_id: int):
#     db = SessionLocal()
#     test_user = db.query(Test_User).filter(Test_User.id == test_user_id).first()
#     if test_user:
#         db.delete(test_user)
#         db.commit()
#         db.close()
#         return {"message": "User deleted successfully"}
#     else:
#         db.close()
#         raise HTTPException(status_code=404, detail="User not found")
