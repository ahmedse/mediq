from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .schemas import ServiceRequestResponse, ServiceRequestCreate
from .services import TextProcessingService
from .config import config
from .models import ServiceType
import logging.config

# Configure logging
logging.config.fileConfig(config.LOGGING_CONFIG_PATH)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Setup CORS middleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Create a router instance
router = APIRouter()

@router.post("/process_text/", response_model=ServiceRequestResponse)
async def process_text(service_request: ServiceRequestCreate, db: Session = Depends(database.get_db)):
    # Assuming service_request is an object with a service_type attribute    
    try:
        service_type_enum = ServiceType(service_request.service_type)
    except ValueError as e:
        logger.error(f"Invalid service type: {service_request.service_type}")
        raise HTTPException(status_code=400, detail="Invalid service type provided")
   
    # Create an instance of TextProcessingService with the enum and text
    service = TextProcessingService(
        service_type=service_type_enum.name, 
        text=service_request.text,
        academic_year=service_request.academic_year if hasattr(service_request, 'academic_year') else None,
        course_code=service_request.course_code if hasattr(service_request, 'course_code') else None,
        course_title=service_request.course_title if hasattr(service_request, 'course_title') else None,
        lecture_title=service_request.lecture_title if hasattr(service_request, 'lecture_title') else None,
        topic=service_request.topic if hasattr(service_request, 'topic') else None,
        user_prompt=service_request.user_prompt if hasattr(service_request, 'user_prompt') else None)
    
    try:
        # Process the text with the service
        context_prompt, user_response, processing_time = service.process_text()
        logger.info(f"Processed text: {user_response}, Processing time: {processing_time}")

        # Create response object according to ServiceRequestResponse schema
        response_object = ServiceRequestResponse(
            id= service.id,
            context_prompt=service.context_prompt,
            user_response=service.user_response,
            processed_successfully=True,
            processing_time=service.processing_time
        )
        return response_object
    except Exception as e:
        # Log the error and raise an HTTPException with the details
        logger.error(f"Error processing text: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Include the router in the app
app.include_router(router)

# Add more endpoints as needed