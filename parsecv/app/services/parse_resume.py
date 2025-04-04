import re
import unicodedata
from typing import BinaryIO

from app.logging_config import logger
from app.models import (
    Applicant,
    Education,
    Experience,
    ParsingException,
    Resume,
    Skills,
)
from app.ner_model.load_model import nlp
from app.services.text_extrator_service import call_pdf_extractor

CHAR_REPLACEMENTS = {
    "\u00a0": " ",  # weird space
    "\u00b7": "-",  # dot
    "\u2013": "-",  # en dash
    "\u2019": "'",  # single quote
    "\ufb01": "fi",  # fi
    "\ufb02": "fl",  # fl
    "\u0000": "",  # null
}


def clean_text(text):
    normalized = unicodedata.normalize("NFKC", text)
    for char, replacement in CHAR_REPLACEMENTS.items():
        normalized = normalized.replace(char, replacement)
    return re.sub(r"\s+", " ", normalized).strip()


# Uses resume_ner_model to parse resume and build the Resume response
def parse_resume(file: BinaryIO):
    # Calls Extractor service to extract text from pdf
    extractor_response = call_pdf_extractor(file)

    if extractor_response.status_code != 200:
        logger.error(f"Error calling text extractor: {extractor_response.json()}")
        raise ParsingException(
            status=500,
            detail="There was an error calling the backend text extractor service",
        )

    # Cleans text and normalizes characters
    resume_text = clean_text(extractor_response.text)

    logger.debug("Parsing file with NER model")
    # Uses SpaCy model to parse resume
    doc = nlp(resume_text)

    # Initialize resume section variables
    experience_items = []
    education_items = []
    skills = Skills()
    applicant = Applicant()
    overview = ""

    # Labels to check against when parsing
    skill_labels = ["PROG_LANG", "FRAMEWORK", "DATABASE", "DEVOPS", "DEV_TOOL"]
    applicant_labels = [
        "CONTACT_EMAIL",
        "CONTACT_PHONE",
        "GITHUB",
        "LINKEDIN",
        "WEBSITE",
    ]

    # Used when processing block of job description items
    processing_descriptions = False
    needs_description = 0

    logger.debug("Building resume response")
    for ent in doc.ents:
        if ent.label_.startswith("JOB_"):
            # If description block ends, increment counter to next experience object
            if processing_descriptions and not ent.label_ == "JOB_DESC_ITEM":
                processing_descriptions = False
                needs_description += 1
            else:
                processing_descriptions = ent.label_ == "JOB_DESC_ITEM"

            # To track if label has been assigned to existing experience
            assigned_label = False

            if not experience_items:
                experience_items.append(Experience())

            # If parsing description block, add to current needs_description object
            if processing_descriptions:
                experience_items[needs_description].process_label(ent)
            else:
                # Loop through the list if experience objects and add label to first that
                # doesn't contain the current label
                for exp in experience_items:
                    if exp.process_label(ent):
                        assigned_label = True
                        break

                # If no label was assigned, create a new experience object
                if not assigned_label:
                    new_experience = Experience()
                    new_experience.process_label(ent)
                    experience_items.append(new_experience)
        elif ent.label_.startswith("EDU_"):
            assigned_label = False

            if not education_items:
                education_items.append(Education())

            # Loop through list of experience objects and add label to first that
            # doesn't contain the current label
            for edu in education_items:
                if edu.process_label(ent):
                    assigned_label = True
                    break
            # If label was not assigned, create a new education object
            if not assigned_label:
                new_education = Education()
                new_education.process_label(ent)
                education_items.append(new_education)

        elif ent.label_ in skill_labels:
            skills.process_label(ent)
        elif ent.label_ in applicant_labels:
            applicant.process_label(ent)
        elif ent.label_ == "OVERVIEW":
            overview = ent.text

    # Builds and returns Resume response object
    resume = Resume(
        info=applicant,
        overview=overview,
        skills=skills,
        experience=experience_items,
        education=education_items,
    )

    return resume
