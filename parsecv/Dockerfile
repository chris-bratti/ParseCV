FROM python:3.11-slim

WORKDIR /app

COPY ./ /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8282

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8282"]
