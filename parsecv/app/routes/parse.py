from app.models import ParsingException, Resume
from app.services import hashed_password, parse_resume
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import APIKeyHeader

router = APIRouter()

header_scheme = APIKeyHeader(name="apiKey")
ph = PasswordHasher()


@router.post("/parse")
async def parse(
    resume: UploadFile = File(...), api_key: str = Depends(header_scheme)
) -> Resume:
    try:
        ph.verify(hashed_password, api_key)
    except VerifyMismatchError:
        raise ParsingException(status=401, message="Invalid auth credentials")
    if resume.content_type != "application/pdf":
        raise ParsingException(status=400, message="File must be a PDF")

    return parse_resume(resume.file)
