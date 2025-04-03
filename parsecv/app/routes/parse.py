from fastapi import APIRouter, File, UploadFile, Depends
from app.models import Resume
from app.services import parse_resume
from app.models import ParsingException
from fastapi.security import APIKeyHeader
from argon2 import PasswordHasher
from app.services import hashed_password

router = APIRouter()

header_scheme = APIKeyHeader(name="apiKey")
ph = PasswordHasher()

@router.post("/parse")
async def parse(resume: UploadFile = File(...), api_key: str = Depends(header_scheme)) -> Resume:
    try:
        ph.verify(hashed_password, api_key)
    except:
        raise ParsingException(status=401, message="Invalid auth credentials")
    if resume.content_type != "application/pdf":
        raise ParsingException(status=400, message="File must be a PDF")
    
    return parse_resume(resume.file)