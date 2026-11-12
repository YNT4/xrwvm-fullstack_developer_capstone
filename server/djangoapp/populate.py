
import json
from pathlib import Path

from django.db import transaction
from .models import CarMake, CarModel


def initiate():
    data_file = (
        Path(__file__).resolve().parent.parent
        / "database"
        / "data"
        / "car_records.json"
    )

    with data_file.open("r", encoding="utf-8") as file:
        cars = json.load(file)["cars"]

    created_makes = 0
    created_models = 0

    with transaction.atomic():
        for car in cars:
            make, make_created = CarMake.objects.get_or_create(
                name=car["make"],
                defaults={
                    "description": f"{car['make']} car manufacturer"
                }
            )

            if make_created:
                created_makes += 1

            _, model_created = CarModel.objects.get_or_create(
                car_make=make,
                name=car["model"],
                year=int(car["year"]),
                defaults={
                    "type": car["bodyType"]
                }
            )

            if model_created:
                created_models += 1

    print(
        f"Car data initialized: "
        f"{created_makes} makes and "
        f"{created_models} models created."
    )
