# Импортирование библиотек

from fastapi import FastAPI, Depends, HTTPException, Request, Cookie, Response
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, literal_column, join
from jose import JWTError, jwt
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from typing import Optional
import json
from passlib.context import CryptContext

# Импортирование классов из файла

from models import Doctor, Block, Diagnosis, Gender, Inspect, Patient, Place_Insp, Symptoms, User

# Подключение к PostgreSQL

engine = create_engine("postgresql://postgres:1234@localhost/new_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание веб-приложения

app = FastAPI()

# Зависимость для аутентификации

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Подключение CORS механизма

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Секретный ключ для подписи токена (в реальном приложении следует использовать более сложные меры безопасности)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Зависимость для получения текущего пользователя из базы данных

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user is None:
        raise credentials_exception
    return user

# Function to create access token

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/cookie") 
async def login_for_access_token(response:Response, username:str, password:str):
    db = SessionLocal()
    user = db.query(User).filter(User.user_name == username).first()
    db.close() 

    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password. Неверное имя пользователя или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"sub": user.user_name, "lvl": user.lvl}
    response.set_cookie(key="access_cookie", value=f"Bearer {create_access_token(token_data)}")
    return create_access_token(token_data)

# Authentication and token generation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

# Example route with authentication required

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Для пользователей

@app.post("/users/reg", tags=["Users"])
async def get_user(last_name: str, first_name: str, password: str, user_name: str):
    db = SessionLocal()
    new_user = db.query(User).filter(user_name == User.user_name).first()
    if new_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already taken")
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
        if check_user.password == check.password:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=400, detail="Invalid username or password")
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    pass


# Для врачей

@app.get("/doctors", tags=["doctors"])
def get_all_doctors():
    db = SessionLocal()
    a = {"doctor": db.query(Doctor).all()}
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
async def add_inspect(place: str, date: str, doctor: str, patient: str, symptom: str, diagnosis: str, prescriptions: str):
    db = SessionLocal()
    new_inspect = Inspect(place = place, date = date, doctor = doctor, patient = patient, symptom = symptom, diagnosis = diagnosis, prescriptions = prescriptions)
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