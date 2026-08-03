from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:destination_id>/', views.book_destination, name='book_destination'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('qr-submit/', views.qr_payment_submit, name='qr_payment_submit'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('booking-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path("delete-review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("edit-review/<int:review_id>/", views.edit_review, name="edit_review"),
]