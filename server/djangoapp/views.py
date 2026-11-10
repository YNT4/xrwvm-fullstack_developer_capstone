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
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User 
 
 
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
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
def logout_request(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET method required"},
            status=405
        )

    username = (
        request.user.username
        if request.user.is_authenticated
        else ""
    )

    logout(request)

    return JsonResponse({
        "userName": username,
        "status": "Logged out"
    })

# Create a `registration` view to handle sign up request

@csrf_exempt
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
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
