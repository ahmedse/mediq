from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .models import ServiceType

# Enum for service types, mirroring the SQLAlchemy enum
class ServiceType(str, Enum):
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

# Schema for creating a service request
class ServiceRequestCreate(BaseModel):
    class Config(ConfigDict):
        arbitrary_types_allowed = True
    user_id: int = 2329987645
    academic_year: Optional[str] = "year 3"
    course_code: Optional[str] = "MED321"
    course_title: Optional[str] = "Internal Medicine II"
    lecture_title: Optional[str] = "Blood Transfusion"
    topic: Optional[str] = "Blood Transfusion"
    text: str = """Rh immune globulin.
                    Available in IM and IV forms.
                    Indications:
                    -Prevention of development of anti-D by pregnant Rh negative women with Rh positive fetuses and subsequent hemolytic disease of the newborn (HDN).
                    - IV form is used in the treatment of ITP
                    Albumin.
                    Indications:
                    - Hypovolemia: volume expansion.
                    - Acute liver failure: osmotic pressure"""
    user_prompt: Optional[str] = "I need to understand the topic in a simple, easy explanation."
    service_type: ServiceType = ServiceType.TRANSLATION

# Schema for the service request response
class ServiceRequestResponse(BaseModel):
    class Config(ConfigDict):
        arbitrary_types_allowed = True
    id: int
    context_prompt: str
    user_response: str
    processed_successfully: bool
    processing_time: Optional[float]

    class Config:
        from_attributes = True

# Schema for collecting user feedback
class ServiceRequestFeedback(BaseModel):
    class Config(ConfigDict):
        arbitrary_types_allowed = True
    id: int
    user_feedback: Optional[str]
    response_grade: Optional[float]