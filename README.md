# ParseCV

A FastAPI-powered resume parsing service using a custom-trained SpaCy NER model to extract structured information from PDF resumes

## Text Extractor service

This API requires the [TextExtractor](https://github.com/chris-bratti/text-extractor) backend service.

One of the most important parts of the resume parsing process is a library for accurately extracting text from a PDF. Unfortunately, none of the Python libraries I tried were able to consistently handle the formatting
that is typically seen in resumes. I decided to try an option outside of Python, and Apache PDFBox was able to give me the most consistent results. I decided to move the logic of text extraction to the `TextExtractor` 
Spring Boot API so I could get the best results possible.

## Running locally

#### Create a Virtual Environment and install dependencies

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

#### Run the FastAPI server

```bash
cd parsecv

uvicorn app.main:app --reload --host 0.0.0.0 --port 8282
```

## API Usage

### OpenAPI
When running locally, you can view the OpenAPI docs at `localhost:8282/docs`

### Parsing a resume
Ensure the `TextExtractor` API is running at `localhost:8081`

Endpoint: `POST /api/parse` <br>
Accepts an `application/pdf` file and returns extracted resume information

Example cURL:
```bash
curl -x 'POST' 'http://localhost:8282/api/parse` \
-H 'accept: application/json` \
-F 'file=@resume.pdf
```

Example response:

```json
{
    "info": {
        "name": "John Smith",
        "phone": "(123) 456 7890",
        "email": "john@smith.com",
        "github": "github.com/johnsmith",
        "linkedin": "linkedin.com/in/johnsmith",
        "website": "www.johnsmith.com"
    },
    "skills": {
        "languages": [
            "Python",
            "Java",
        ],
        "frameworks": [
            "Spring Boot",
            "FastAPI",
        ],
        "devops": [
            "Kubernetes",
            "Docker",
        ],
        "database": [
            "SQL",
            "SQL Server",
        ],
        "dev_tools": [
            "Git",
            "GitHub",
            "OpenAPI",
        ]
    },
    "overview": "Software engineer with 10 years of experience designing and implementing back-end systems in Java and Python",
    "experience": [
        {
            "company": "Company B",
            "title": "Senior Software Engineer",
            "duration": "Jan 2020 - Present",
            "location": "New York, NY",
            "desc": [
                "Develop Spring Boot APIs",
                "Develop FastAPI applications",
                "Mentor junior employees"
            ]
        },
        {
            "company": "Company A",
            "title": "Junior Software Engineer",
            "duration": "Jan 2015 - Jan 2020",
            "location": "Boston, MA",
            "desc": [
                "Worked with senior developers to design Java applications",
                "Implemented unit tests",
                "Learned a lot of things"
            ]
        }
    ],
    "education": [
        {
            "college": "Harvard University",
            "degree": "Masters of Science",
            "major": "Computer Science"
        },
        {
            "college": "Yale University",
            "degree": "Bachelor of Science",
            "major": "Computer Science"
        }
    ]
}
```

## NER Model
The NER model is located in `parsecv/app/ner_model/resume_ner_model`

I'm still actively training this model, so the parsing results may vary depending on the resume's content and formatting. It currently handles the job experience sections pretty well, but has some problems identifying 
personal info (name, email, etc) and company names. This should improve with time as the model gets more training.

If you would like to retrain the model, use the resources in the `ner_training` module. You'll need the `TextExtractor` API running to create the SpaCy test data.

## Example client

This API is currently being used by my [website](https://github.com/chris-bratti/chrisbratti-website) to populate the webpage with information from my resume. Check it out to see the API in action!
