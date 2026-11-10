# Uncomment the imports below before you add the function code
import os
import requests 
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", "http://localhost:3030")

sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    request_url = (
        backend_url.rstrip("/")
        + "/"
        + endpoint.lstrip("/")
    )

    try:
        response = requests.get(
            request_url,
            params=kwargs,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Backend request failed: {error}")
        return None

# def get_request(endpoint, **kwargs):
# Add code for get requests to back end

# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

# def post_review(data_dict):
# Add code for posting review
