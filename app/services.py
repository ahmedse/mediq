from .models import ServiceType
from typing import Optional
from openai import OpenAI
import time
import os
from sqlalchemy.orm import Session
from . import crud
import logging
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
logger = logging.getLogger(__name__)

class TextProcessingService:
    def __init__(
        self, 
        service_type: str, 
        text: str,
        academic_year: Optional[str] = None,
        course_code: Optional[str] = None,
        course_title: Optional[str] = None,
        lecture_title: Optional[str] = None,
        topic: Optional[str] = None,
        user_prompt: Optional[str] = None
    ):
        self.service_type = service_type
        self.text = text
        self.academic_year = academic_year
        self.course_code = course_code
        self.course_title = course_title
        self.lecture_title = lecture_title
        self.topic = topic
        self.user_prompt = user_prompt

        # 
        self.openai_api_key = "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"

    def process_text(self):             
        db = SessionLocal()
        service_request_data = {
            'user_id': 2329987645,
            'service_type': self.service_type,
            'text': self.text,
            'academic_year': self.academic_year,
            'course_code': self.course_code,  # Fixed this line
            'course_title': self.course_title,  # And this line
            'lecture_title': self.lecture_title,
            'topic': self.topic,
            'user_prompt': self.user_prompt,
        }

        try:
            service_request = crud.create_service_request(db, service_request_data)            
            # ... [rest of the logic for processing the request]

        except SQLAlchemyError as e:
            print(f"Database operation failed: {e}")
            # Log the error and the input data that caused it
            logger.error(f"Database operation failed: {e}")
            logger.error(f"Failed data: {service_request_data}")
            db.rollback()  # Rollback the session in case of error
            return None  # You may want to return an error message or code instead
        # finally:
        #     db.close()  # Ensure the db session is closed after the operation
                      
        db.refresh(service_request)
        self.id= service_request.id
        
        # Implement the logic for different service types
        if self.service_type == ServiceType.TRANSLATION.name:            
            self.context_prompt, self.user_response, self.processing_time = self._handle_translation()

            # update the service request data
            service_request.context_prompt = self.context_prompt
            service_request.user_response = self.user_response
            service_request.processing_time = self.processing_time
            db.add(service_request)
            db.commit()
            
            return self.context_prompt, self.user_response, self.processing_time
        # Add other service type handlers as needed
        else:
            raise ValueError("Unsupported service type")

    def _handle_translation(self):   
        
        context_prompt = self.construct_prompt_inputs()

        client = OpenAI(
            # This is the default and can be omitted
            # api_key=os.environ.get("OPENAI_API_KEY"),
            api_key= self.openai_api_key,
        )

        try:
            # Start timing
            start_time = time.time()
            # Call the OpenAI API with the prompt
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "You are an explanation and translation assistant in medicine education."},
                    {"role": "user", "content": f"{context_prompt}"}
                ]
            )
            print(f"response: {response}")  
            # End timing
            processing_time = time.time() - start_time
            # Extract the response text
            generated_raw= response.choices[0].message.content

            # here do post-processing of returned raw data. 
            translated_text=  generated_raw

            return context_prompt, translated_text, processing_time, generated_raw
        except Exception as e:
            # Handle API errors
            print(f"Error calling OpenAI API: {str(e)}")
            raise e  # Or handle it in another way appropriate for your application
        return None, None, None, None
    
    # ... other private methods for handling specific services

    def construct_prompt_inputs(self) -> str:
        # Construct the prompt based on the instance attributes
        prompt_inputs = [
            f"Your task is to: {self.service_type}" if self.service_type else "Explain"
            f"Medicine Student at Academic Year: {self.academic_year}" if self.academic_year else "3",
            f"Course Title: {self.course_title}" if self.course_title else "",
            f"Lecture Title: {self.lecture_title}" if self.lecture_title else "",
            f"Topic: {self.topic}" if self.topic else "",
            f"Text: {self.text}" if self.text else "",
            f"Additional User Prompt: {self.user_prompt}" if self.user_prompt else "",
            f"Explain in scientifically accurate tone for the student to understand and then translate to Arabic, don't hesitate to use en terms if necessary",
        ]

        # Filter out any empty strings and join the remaining parts with newlines
        prompt = "\n".join(filter(None, prompt_inputs))
        
        return prompt
    
    