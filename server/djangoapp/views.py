# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
import requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .restapis import get_request
from .models import CarMake, CarModel
from .restapis import get_request, backend_url
from django.views.decorators.csrf import ensure_csrf_cookie
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
def login_user(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = data.get("userName", "")
    password = data.get("password", "")

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)

        return JsonResponse({
            "userName": username,
            "status": "Authenticated"
        })

    return JsonResponse({
        "userName": username,
        "status": "Failed",
        "message": "Invalid username or password"
    }, status=401)

from pathlib import Path
from django.conf import settings
from django.http import HttpResponse


def serve_static_page(filename):
    file_path = (
        Path(settings.BASE_DIR)
        / "frontend"
        / "static"
        / filename
    )

    if not file_path.is_file():
        return HttpResponse("Page not found", status=404)

    return HttpResponse(
        file_path.read_text(encoding="utf-8"),
        content_type="text/html; charset=utf-8"
    )


def about(request):
    return serve_static_page("About.html")


def contact(request):
    return serve_static_page("Contact.html")
# Create a `logout_request` view to handle sign out request
# Handle user logout
def logout_request(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET method required"},
            status=405
        )

    logout(request)

    return JsonResponse({
        "userName": "",
        "status": "Logged out"
    })

# Create a `registration` view to handle sign up request
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = data.get("userName", "").strip()
    first_name = data.get("firstName", "").strip()
    last_name = data.get("lastName", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not all([username, first_name, last_name, email, password]):
        return JsonResponse(
            {"error": "All fields are required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "Username already exists"},
            status=409
        )

    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse(
            {"error": "Email already exists"},
            status=409
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    return JsonResponse({
        "userName": user.username,
        "status": "Registered"
    }, status=201)


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET method required"},
            status=405
        )

    dealerships = get_request("fetchDealers")

    if dealerships is None:
        return JsonResponse(
            {"error": "Unable to retrieve dealerships"},
            status=502
        )

    return JsonResponse(
        {"dealers": dealerships},
        status=200
    )

# Create a `get_dealer_reviews` view to render the reviews of a dealer



def get_dealer_reviews(request, dealer_id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET method required"},
            status=405
        )

    reviews = get_request(
        f"fetchReviews/dealer/{dealer_id}"
    )

    if reviews is None:
        return JsonResponse(
            {"error": "Unable to retrieve dealer reviews"},
            status=502
        )

    return JsonResponse({
        "reviews": reviews
    })

def get_dealer_by_id(request, dealer_id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET method required"},
            status=405
        )

    dealer = get_request(f"fetchDealer/{dealer_id}")

    if dealer is None:
        return JsonResponse(
            {"error": "Unable to retrieve dealer"},
            status=502
        )

    return JsonResponse(
        {"dealer": dealer},
        status=200
    )
def get_cars(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET method required"},
            status=405
        )

    car_makes = CarMake.objects.prefetch_related(
        "car_models"
    ).all().order_by("id")

    result = []
    car_models = []

    for make in car_makes:
        models = []

        for car in make.car_models.all():
            models.append({
                "id": car.id,
                "name": car.name,
                "type": car.type,
                "year": car.year
            })

            car_models.append({
                "CarMake": make.name,
                "CarModel": car.name
            })

        result.append({
            "id": make.id,
            "name": make.name,
            "description": make.description,
            "models": models
        })

    return JsonResponse(
        {
            "CarModels": car_models,
            "car_makes": result
        },
        status=200
    )
def get_session(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "isAuthenticated": True,
            "username": request.user.username
        })

    return JsonResponse({
        "isAuthenticated": False,
        "username": None
    })
# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):

@login_required
@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405
        )

    try:
        data = json.loads(request.body)

        required_fields = [
            "dealership",
            "review",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year"
        ]

        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {"error": f"Missing field: {field}"},
                    status=400
                )

        review_data = {
            "name": request.user.get_full_name()
                    or request.user.username,
            "dealership": int(data["dealership"]),
            "review": data["review"],
            "purchase": True,
            "purchase_date": data["purchase_date"],
            "car_make": data["car_make"],
            "car_model": data["car_model"],
            "car_year": int(data["car_year"])
        }

        response = requests.post(
            f"{backend_url.rstrip('/')}/insert_review",
            json=review_data,
            timeout=10
        )

        response.raise_for_status()

        return JsonResponse({
            "status": 200,
            "message": "Review added successfully",
            "review": response.json()
        })

    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        return JsonResponse(
            {"error": str(error)},
            status=400
        )

    except requests.RequestException as error:
        return JsonResponse(
            {"error": str(error)},
            status=502
        )
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({
        "message": "CSRF cookie set"
    })