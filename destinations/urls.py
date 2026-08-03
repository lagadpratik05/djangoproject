from django.urls import path
from .views import destinations_list, destination_detail
from bookings.views import my_bookings, cancel_booking

from . import views


urlpatterns = [
    path("", destinations_list, name="destinations"),
    path("<int:pk>/", destination_detail, name="destination_detail"),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path("<int:pk>/", views.destination_detail, name="destination_detail"),

    path('add/', views.add_destination, name='add_destination'),
    path('edit/<int:id>/', views.edit_destination, name='edit_destination'),
    path('delete/<int:id>/', views.delete_destination, name='delete_destination'),

]
