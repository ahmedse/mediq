# app/models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum, DateTime, Boolean, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum

Base = declarative_base()

# Enum for service types
class ServiceType(enum.Enum):
    TRANSLATION = "Translation"
    SUMMARIZATION = "Summarization"
    SIMPLIFICATION = "Simplification"

    MEDICAL_TERM_DEFINITION = "Medical Term Definition Extraction"
    DRUG_INTERACTION_SUMMARY = "Drug Interaction Summarization"
    CASE_STUDY_HIGHLIGHT = "Case Study Highlighter"
    DIAGNOSTIC_CRITERIA_CHECKLIST = "Diagnostic Criteria Checklist"
    TREATMENT_PLAN_GENERATION = "Treatment Plan Generation"
    CLINICAL_GUIDELINE_SUMMARY = "Clinical Guideline Summarization"
    RESEARCH_PAPER_SUMMARY = "Research Paper Summarization"
    QUESTION_GENERATION = "Question Generation"
    EVIDENCE_GRADING = "Evidence Grading"
    SYMPTOM_CHECKER = "Symptom Checker"
    PROCEDURE_SIMPLIFICATION = "Procedure Step-By-Step Simplification"

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to the User table
    user = relationship("User", back_populates="service_requests")  # ORM relationship
    academic_year = Column(String)
    course_code = Column(String)
    course_title = Column(String)
    lecture_title = Column(String)
    topic = Column(String)
    text = Column(String)
    user_prompt = Column(String)
    service_type = Column(String)  # "translation", "summarization", "simplification"

    # constructed prompt that will be sent to ex. chatgp.
    context_prompt = Column(String)
    
    # chatgpt raw results.
    generated_raw = Column(String)

    # shaped and processed response from mediq to the user
    user_response = Column(String)

    processed_successfully = Column(Boolean, default=True)  # Whether the text was processed successfully

    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp when the record was created
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Timestamp when the record was last updated    
    processing_time = Column(Integer)

    # feedback from user.
    user_feedback = Column(Text, nullable=True)  # Text feedback from the user
    response_grade = Column(Numeric(2, 1), nullable=True)  # Numerical grading of the response, e.g., scale of 1.0-5.0

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    total_messages = Column(Integer, default=0)  # Total number of messages sent since account creation
    weekly_quota = Column(Integer, default=200)  # Weekly quota for service requests
    quota_used = Column(Integer, default=0)  # Number of service requests used in the current week
    quota_reset_date = Column(DateTime)  # The date and time when the quota will reset next
    created_at = Column(DateTime, default=func.now())
    service_requests = relationship("ServiceRequest", back_populates="user")  # ORM relationship