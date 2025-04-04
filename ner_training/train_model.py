import argparse
import json
import random

import spacy
from spacy.training import Example


def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# Trains the NER model using the provided training data
def train_ner_model(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank("en")

    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities", []):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        nlp.initialize()

        for itn in range(iterations):
            print(f"Starting iteration {itn + 1}")
            random.shuffle(TRAIN_DATA)
            losses = {}

            for text, annotations in TRAIN_DATA:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], losses=losses, drop=0.2)

            print(f"Losses at iteration {itn + 1}: {losses}")
    return nlp


arg_parser = argparse.ArgumentParser(description="Script to train ner model")

arg_parser.add_argument("training_data_path", type=str, help="Path to training data")

args = arg_parser.parse_args()

if args.training_data_path is None:
    raise Exception("Path to training data required!")

TRAIN_DATA = load_json(args.training_data_path)

nlp = train_ner_model(TRAIN_DATA, 60)
nlp.to_disk("resume_ner_model")
