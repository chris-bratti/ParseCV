import argparse
import json
import os
import re
import unicodedata

import requests
import spacy
from spacy.training import offsets_to_biluo_tags


# Calls the Text Extractor API to extract text from the PDF
def extract_text(pdf_path: str):
    with open(pdf_path, "rb") as file:
        files = {"file": (pdf_path, file, "application/pdf")}
        response = requests.post(url, files=files)
    return response


url = "http://localhost:8081/extract"


def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_data(file_path: str, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


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


# Converts the label studio JSON to the SpaCy format
def convert_labelstudio_to_spacy(labelstudio_json):
    spacy_data = []
    trailing_regex = r"[\s.]"

    for entry in labelstudio_json:
        text = clean_text(entry["text"])
        annotations = entry["label"]

        entities = []

        for annotation in annotations:
            start, end = annotation["start"], annotation["end"]
            label = annotation["labels"][0]

            # Adjust start position if it lands on whitespace/punctuation
            while start < len(text) and re.match(trailing_regex, text[start]):
                start += 1

            # Adjust end position to avoid cutting words
            while end > 0 and re.match(trailing_regex, text[end - 1]):
                end -= 1

            # Ensure valid range before adding
            if start < end and 0 <= start < len(text) and 0 < end <= len(text):
                entities.append((start, end, label))

        spacy_data.append((text, {"entities": entities}))

    return spacy_data


# Verifies generated training data is properly aligned
def verify_test_data(TRAIN_DATA):
    nlp = spacy.blank("en")
    data_pass = True

    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        biluo_tags = offsets_to_biluo_tags(doc, annotations["entities"])

        if "-" in biluo_tags:
            print("\nERROR: Misaligned Entity Found:")
            print("TEXT:", text[:20])
            data_pass = False

    return data_pass


# Extracts text from PDFs in the input folder and saves them to the output folder
def parse_resumes():
    input_dir = "resumes/input"
    output_dir = "resumes/output"
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_text = extract_text(f"{input_dir}/{file}").text
            pdf_text = clean_text(pdf_text)
            save_data(f"{output_dir}/{file.replace('.pdf', '.txt')}", pdf_text)


# Generates and saves the training data
def generate_test_data(label_studio_path: str):
    test_data_name = "full_resume_training_data.json"

    labelstudio_json = load_json(label_studio_path)

    output = convert_labelstudio_to_spacy(labelstudio_json)

    if verify_test_data(output):
        save_data(f"training_data/{test_data_name}", output)
        print(f"Data was saved as {test_data_name}")
    else:
        print("Data was not saved due to validation errors")


arg_parser = argparse.ArgumentParser(
    description="Script to automate generating test data"
)

arg_parser.add_argument("command", type=str, help="Command [extract | generate]")
arg_parser.add_argument(
    "label_studio_input", type=str, nargs="?", help="Path to Label Studio data"
)

args = arg_parser.parse_args()

match args.command:
    case "extract":
        parse_resumes()
    case "generate":
        label_studio_input = args.label_studio_input
        if label_studio_input is not None:
            generate_test_data(label_studio_input)
        else:
            print("'generate' command requires label_studio_path")
