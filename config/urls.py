from django.urls import path

from booking.views import create_booking

urlpatterns = [path("api/bookings/", create_booking)]
