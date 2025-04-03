# NER Training

## Data and scripts to train resume NER model

### Retraining the NER model

Basic steps:

1. Place PDF resumes to use to train the model in `ner_training/resumes/input`
2. Start the `TextExtractor` API
3. Run `create_test_data.py extract`, this will extract the text from the PDFs and output them to `ner_training/resumes/output/<file_name>.txt`
4. Use [Label Studio](https://labelstud.io/) to label the data, and export using the JSON-Mini format
5. Run `create_test_data.py generate /path/to/label_studio.json`, this will transform the Label Studio JSON output to the SpaCy format
6. Run `train_model.py training_data/full_resume_training_data.json` (If you've moved the SpaCy JSON file make sure to update the command)
7. The new model can be found at `ner_training/resume_ner_model`!