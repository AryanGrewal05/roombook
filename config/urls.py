from django.http import JsonResponse
from django.urls import path

from booking.views import create_booking


def home(request):
    return JsonResponse({
        "app": "RoomBook",
        "status": "running",
        "message": "Welcome to the CSC325 RoomBook API",
        "endpoints": ["/api/bookings/", "/api/status/"],
    })


def room_status(request):
    return JsonResponse({
        "service": "RoomBook",
        "status": "available",
        "version": "module8-demo",
        "message": "Room booking service is available",
    })


urlpatterns = [
    path("", home, name="home"),
    path("api/bookings/", create_booking),
    path("api/status/", room_status, name="room_status"),
]
