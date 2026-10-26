from django.http import JsonResponse
from django.urls import path

from booking.views import create_booking


def home(request):
    return JsonResponse({
        "app": "RoomBook",
        "status": "running",
        "message": "Welcome to the CSC325 RoomBook API",
        "endpoints": ["/api/bookings/"]
    })


urlpatterns = [
    path("", home, name="home"),
    path("api/bookings/", create_booking),
]
