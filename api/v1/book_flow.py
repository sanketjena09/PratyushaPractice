import traceback
from typing import Optional
from urllib import response
from fastapi import APIRouter, Depends, FastAPI,Path,Response,status,HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from requests import Session
from sqlalchemy.orm import Session
import models
import schemas
# from .import models,schemas
from database import engine,SessionLocal
# from utils.fb_utils import decrypt_request, encrypt_response
from core.keys import PHONE_NUMBER_PRIVATE_KEY
from utils.fb_utils import decrypt_request, encrypt_response
from utils.reg_utils import decode_payload, encode_payload, response_generate
from datetime import datetime
from database import get_db

def calculate_age(dob):
            today = datetime.today()
            dob = datetime.strptime(dob, "%Y-%m-%d")  # Format: YYYY-MM-DD
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            print(dob)
            print(age)
            return age
        

pratyusha_router = APIRouter()

@pratyusha_router.post("/book_flow")
async def book_flow(body: dict):
    status_active = {
        "data": {
            "status":"active"
        }
    }
    
    
    try:
        decoded_payload = decode_payload(body)
        print("payload", decoded_payload)
        
        
        

        
        all_patients=[
                {
                    "id": "1",
                    "title": "Rahul"
                },
                {
                    "id": "2",
                    "title": "Virat"
                }
        ]
        
        # all_doctors = [
        #         {
        #             "id": "1",
        #             "title": "riya"
        #         },
        #         {
        #             "id": "2",
        #              "title": "jasmin"
        #         }
        # ]
        
        all_location = [
                {
                     "id": "1",
                    "title": "patia"
                },
                {
                    "id": "2",
                    "title": "khandagiri"
                }
        ]
        
        appointment_type =[
                {
                    "id": "1",
                    "title": "Online"
                },
                {
                    "id": "2",
                    "title": "In Person"
                }
        ]
        
        all_symptoms =[
               {
                    "id": "1",
                    "title": "Cough"
                },
                {
                    "id": "2",
                    "title": "Chest Pain"
                },
                {
                    "id": "3",
                    "title": "Breathing issues"
                },
                {
                    "id": "4",
                    "title": "Allegic"
                }
        ]
        
        if decoded_payload["action"] == 'ping':
            return response_generate(body, status_active)
    
        elif decoded_payload['action'] == 'INIT':
            response_payload = {
                    "screen": 'WELCOME_SCREEN',
                    "data" : {
                        "patient_list":False              
                    }
                }
            
        
        elif decoded_payload['action'] == 'data_exchange':
            db= SessionLocal()
            payload_data = decoded_payload['data']
            phone_number = decoded_payload['flow_token']
             
            if 'trigger' in decoded_payload["data"] :
                trigger_type = decoded_payload['data']['trigger']
                if trigger_type == "select_patient":
                    if decoded_payload['data']['patient_type'] == "new":
                        response_payload = {
                            "screen": 'REGISTER',
                            "data":{
                                "max_date": "2025-03-29"
                            }
                        }
                    
                    elif decoded_payload['data']['patient_type'] == "existing":
                        
                        db_patients = db.query(models.Patients).filter(models.Patients.phone == '9999999999').all()
                        return_patient = [{'id':str(patient.id),"title":patient.first_name} for patient in db_patients]
                        print(return_patient)
                        response_payload = {
                            "screen":"WELCOME_SCREEN",
                            "data":{
                                "all_patients": return_patient,
                                "patient_list": True
                            }
                        }
                        
                elif trigger_type == "dob_select":
                    if decoded_payload['data']['dob_date']:
                        age = calculate_age(decoded_payload['data']['dob_date']) if (decoded_payload['data']['dob_date'] != "" ) and (decoded_payload['data']['dob_date'] != 'NaN-NaN-NaN' ) else ""
                        response_payload = {
                            "screen":'REGISTER',
                            "data":{
                                "age": str(age)
                            }
                        }
                
                elif trigger_type == "register_page":
                    register = decoded_payload['data']
                    register.pop("trigger")
                    register.pop("address")
                    register.pop("dob_date")
                    print(register)
                    all_ids = db.query(models.Patients.id).order_by(models.Patients.id).all()
                    last_id = all_ids[-1][0]
                    new_patient = models.Patients(**register,phone=phone_number,id=last_id+1)
                    db.add(new_patient)
                    db.commit()
                    
                    db_doctors= db.query(models.Doctors).all()
                    
                    all_doctors=[{"id":str(doctor.id),"title":doctor.name} for doctor in db_doctors]
                    print(all_doctors)
                    response_payload ={
                        "screen":"APPOINTMENT",
                        "data":{
                            "exist_patient":str(new_patient.id),
                            "all_doctors":all_doctors,
                            "location_visible":False,
                            "symptoms_visible":False,
                            "document_visible":False,
                            "ap_type_visible":False,
                            "date_visible":False,
                            "doc_visible":False
                        }
                    }
                                    
                elif trigger_type == "doctor_select":
                    if decoded_payload['data']['doctor']:
                        response_payload = {
                            "screen":'APPOINTMENT',
                            "data":{
                                "location_visible":True,
                                "all_location" :all_location
                            }
                        }
                        
                elif trigger_type == "location_select":
                    if decoded_payload['data']['location']:
                        response_payload ={
                             "screen":'APPOINTMENT',
                             "data":{
                                 "symptoms_visible":True,
                                 "all_symptoms" : all_symptoms
                             }
                        }
               
                
                elif trigger_type == "symptoms_select":
                    if decoded_payload['data']['symptoms']:
                        response_payload ={
                            "screen":'APPOINTMENT',
                            "data":{
                                # "document_visible":True,
                                # "ap_type_visible":True,
                                # "appointment_type": appointment_type
                               "doc_visible":True
                            }
                        }
                elif trigger_type == "Select_Doc":
                    if decoded_payload['data']['doc'] == "Yes":
                        response_payload={
                            "screen": 'APPOINTMENT',
                            "data":{
                                "document_visible":True,
                                 "ap_type_visible":True,
                                 "appointment_type": appointment_type
                            }
                        }
                    elif decoded_payload['data']['doc'] == "No":
                        response_payload ={
                             "screen": 'APPOINTMENT',
                            "data":{
                                "document_visible": False,
                                "ap_type_visible":True,
                                 "appointment_type": appointment_type
                            }
                        }
                elif  trigger_type == "appointment_select":
                    if decoded_payload['data']['appointment_type']:
                        response_payload = {
                            "screen":'APPOINTMENT',
                            "data":{
                                "date_visible":True
                            }
                        }
                
                if db:
                    db.close()
                  
        return response_generate(body, response_payload)
    
    except Exception as e:
      print("Error: " + str(e))
      traceback.print_exc()
      response_payload = {
                "screen": decoded_payload['screen'],
                "data": {
                    "error": True,
                    "error_message":"Some Error Occured."
                }
            }
    return PlainTextResponse(content=encode_payload(body, response_payload), media_type='text/plain')

    
    

        
