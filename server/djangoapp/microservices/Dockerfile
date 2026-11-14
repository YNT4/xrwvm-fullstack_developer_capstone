
FROM python:3.9-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the bundled VADER lexicon available to NLTK
RUN mkdir -p /usr/local/nltk_data/sentiment && \
    cp sentiment/vader_lexicon.zip /usr/local/nltk_data/sentiment/

ENV NLTK_DATA=/usr/local/nltk_data
ENV FLASK_APP=app.py

EXPOSE 10000

CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=${PORT:-10000}"]
