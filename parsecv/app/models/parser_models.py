from typing import Optional
from spacy.tokens import Span
from pydantic import BaseModel
from typing import Optional, List

class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    desc: Optional[List[str]] = None
    
    def process_label(self, ent: Span):
        match ent.label_:
            case "JOB_COMPANY":
                if self.company is None:
                    self.company = ent.text
                else:
                    return False
            case "JOB_TITLE":
                if self.title is None:
                    self.title = ent.text
                else:
                    return False
            case "JOB_DURATION":
                if self.duration is None:
                    self.duration = ent.text
                else:
                    return False
            case "JOB_DESC_ITEM":
                if self.desc is None:
                    self.desc = []
                
                self.desc.append(ent.text)
            case "JOB_LOCATION":
                if self.location is None:
                    self.location = ent.text
                else:
                    return False
        return True

class Education(BaseModel):
    college: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None

    def process_label(self, ent: Span):
        match ent.label_:
            case "EDU_DEG":
                if self.degree is None:
                    self.degree = ent.text
                else:
                    return False
            case "EDU_COLLEGE":
                if self.college is None:
                    self.college = ent.text
                else:
                    return False
            case "EDU_MAJOR":
                if self.major is None:
                    self.major = ent.text
                else:
                    return False
        
        return True

class Skills(BaseModel):
    languages: Optional[list[str]] = None
    frameworks: Optional[list[str]] = None
    devops: Optional[list[str]] = None
    database: Optional[list[str]] = None
    dev_tools: Optional[list[str]] = None    
    
    def process_label(self, ent: Span):
        match ent.label_:
            case "PROG_LANG":
                if self.languages is None:
                    self.languages = []

                self.languages.append(ent.text)
            case "FRAMEWORK":
                    if self.frameworks is None:
                        self.frameworks = []

                    self.frameworks.append(ent.text)
            case "DEVOPS":
                    if self.devops is None:
                        self.devops = []

                    self.devops.append(ent.text)
            case "DATABASE":
                    if self.database is None:
                        self.database = []

                    self.database.append(ent.text)
            case "DEV_TOOL":
                    if self.dev_tools is None:
                        self.dev_tools = []

                    self.dev_tools.append(ent.text)

class Applicant(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None

    def process_label(self, ent: Span):
        match ent.label_:
            case "NAME":
                self.name = ent.text
            case "CONTACT_EMAIL":
                self.email = ent.text
            case "CONTACT_PHONE":
                self.phone = ent.text
            case "GITHUB":
                self.github = ent.text
            case "LINKEDIN":
                self.linkedin = ent.text
            case "WEBSITE":
                self.website = ent.text

class Resume(BaseModel):
    info: Applicant
    skills: Skills
    overview: str
    experience: list[Experience]
    education: list[Education]