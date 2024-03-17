import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from .models import ServiceRequest
from decimal import Decimal

# Assuming you have already configured logging as described
logger = logging.getLogger(__name__)

# CRUD function to create a service request
def create_service_request(db: Session, service_request_data: dict) -> ServiceRequest:
    try:
        service_request = ServiceRequest(**service_request_data)
        db.add(service_request)
        db.commit()
        db.refresh(service_request)
        return service_request
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating service request: {e}")
        return None

# CRUD function to update a service request
def update_service_request(db: Session, service_request_id: int, update_data: dict) -> ServiceRequest:
    try:
        db.query(ServiceRequest).filter(ServiceRequest.id == service_request_id).update(update_data)
        db.commit()
        return db.query(ServiceRequest).filter(ServiceRequest.id == service_request_id).first()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating service request with id {service_request_id}: {e}")
        return None

# CRUD function to delete a service request
def delete_service_request(db: Session, service_request_id: int) -> bool:
    try:
        service_request = db.query(ServiceRequest).get(service_request_id)
        if service_request:
            db.delete(service_request)
            db.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting service request with id {service_request_id}: {e}")
        return False

# Function to update request processing details
def update_processing_details(db: Session, service_request_id: int, processing_details: dict) -> ServiceRequest:
    try:
        service_request = db.query(ServiceRequest).get(service_request_id)
        if service_request:
            for key, value in processing_details.items():
                setattr(service_request, key, value)
            db.commit()
            db.refresh(service_request)
            return service_request
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating processing details for service request with id {service_request_id}: {e}")
        return None

# Function to save user feedback
def save_user_feedback(db: Session, service_request_id: int, feedback: str, grade: Decimal) -> ServiceRequest:
    try:
        service_request = db.query(ServiceRequest).get(service_request_id)
        if service_request:
            service_request.user_feedback = feedback
            service_request.response_grade = grade
            db.commit()
            db.refresh(service_request)
            return service_request
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error saving user feedback for service request with id {service_request_id}: {e}")
        return None