import spacy
from pathlib import Path
from app.logging_config import logger

MODEL_PATH = Path(__file__).parent / "resume_ner_model"

try:
    nlp = spacy.load(str(MODEL_PATH))
    logger.info("NER model loaded")
except Exception as e:
    raise RuntimeError(f"Failed to load NER model: {e}")