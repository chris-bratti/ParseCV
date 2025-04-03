from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models import Resume
from app.services import parse_resume
from app.models import ParsingException

router = APIRouter()

@router.post("/parse")
async def parse(resume: UploadFile = File(...)) -> Resume:

    if resume.content_type != "application/pdf":
        raise ParsingException(status=400, message="File must be a PDF")
    
    return parse_resume(resume.file)