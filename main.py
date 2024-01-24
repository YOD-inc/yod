# Импортирование библиотек

from fastapi import FastAPI, Depends, HTTPException 
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


# Импортирование классов из файла

from models import Doctor, Block, Diagnosis, Gender, Inspect, Patient, Place_Insp, Symptoms, User


# Подключение к PostgreSQL

engine = create_engine("postgresql://postgres:1234@localhost/new_db")
# engine = create_engine("postgresql://postgres:admin@localhost/test_db")
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


# def get_db():
#     db = SessionLocal()
#     try: 
#         yield db
#     finally:
#         db.close()



# # Функция для получения текущего пользователя из токена

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     db = SessionLocal()
#     user = db.query(User).filter(User.username == username).first()
#     db.close()
#     if user is None:
#         raise credentials_exception
#     return user


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


# OAuth2 scheme for token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to create access token

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Route to get token

@app.post("/token")
async def login_for_access_token(form_data: Auth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.user_name == form_data.username).first()
    db.close() 

    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password. Неверное имя пользователя или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": user.user_name, "lvl": user.lvl}
    return {"access_token": create_access_token(token_data), "token_type": "bearer"}

# Your user and roles models here

# Authentication and token generation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     db = SessionLocal()
#     user = get_user(db, form_data.username)
#     if not user or not verify_password(form_data.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username, "role": user.role},
#         expires_delta=access_token_expires,
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# Protected route

# @app.get("/protected")
# async def protected_route(current_user: User = Depends(get_current_user)):
#     return {"message": "You have access!", "lvl": current_user.lvl}

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

# # Роут для аутентификации

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     # Проведение аутентификации
#     # ...

#     # Генерация JWT токена
#     expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     expires = datetime.utcnow() + expires_delta
#     to_encode = {"sub": username, "exp": expires, "role": user.role}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#     # return {"access_token": access_token, "token_type": "bearer"}
#     return {"access_token": encoded_jwt, "token_type": "bearer", "expires_in": expires_delta.total_seconds()}

# # Роут для обычных пользователей

# @app.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user


# # Роут для модераторов

# @app.get("/moderators/me", response_model=User)
# async def read_moderators_me(current_user: User = Depends(get_current_user)):
#     if current_user.role != "moderator":
#         raise HTTPException(status_code=403, detail="You do not have access to this resource")
#     return current_user


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

@app.get("/doctors", tags=["doctors"])
def get_all_doctors():
    db = SessionLocal()
    a = {"doctor": db.query(Doctor).all()}
    db.close()
    return a

# @app.get("/doctors", tags=["doctors"])
# def get_all_doctors():
#     db = SessionLocal()
#     a = {"inspect_choice_doctor": db.query(
#         select([
#             Doctor.c.id,
#             (Doctor.c.last_n + ' ' + Doctor.c.first_n + ' ' + Doctor.c.patro_n).label('full_n'),
#             Doctor.c.phone_num,
#             Doctor.c.block_id,
#             Doctor.c.exp
#         ])
#         .select_from(Doctor)
#     )}
#     db.close()
#     return a

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
    # a = {"inspect_choice_place": db.query(
    #     select([
    #         Place_Insp.place,
    #     ])
    #     .select_from(Place_Insp)
    # )}
    # db.close()
    # return a

    # a = {"inspect_choice_place": db.query(Place_Insp).all()}

    # b = []
    # for place_name in a["inspect_choice_place"]:
    #     b.append({"place": place_name["place"]})
    # c = {"inspect_choice_place": b}
    # cc = json.dumps(c, indent=2)
    # db.close()
    
    # b = []
    # for Place_Insp in a:
    #     b.append({
    #         "place": Place_Insp.place
    #     })
    # c = json.dumps(b, indent=2)
    a = db.query(Place_Insp.place).all()
    db.close()
    return {"inspect_choice_place": a}

@app.get("/inspect/choice_doctor", tags=["inspect choices"])
def doctor_choice():
    db = SessionLocal()
    # a = {"inspect_choice_doctor": db.query(
    #     select([
    #         (Doctor.c.last_n + ' ' + Doctor.c.first_n + ' ' + Doctor.c.patro_n).label('doctor_full_n')
    #     ])
    #     .select_from(Doctor)
    # )}
    doctors = db.query(Doctor).all()
    full_names = [{"full_name": f"{doctor.last_n} {doctor.first_n}"} for doctor in doctors]
    db.close()
    return {"full_name": full_names}

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
