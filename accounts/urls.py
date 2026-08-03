from django.urls import path, include
from .views import login_view, signup_view, dashboard, logout_view
from .views import profile_view
from accounts import views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('', login_view),  # optional redirect or duplicate

    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    path("profile/", profile_view, name="profile"),
    path("", include("bookings.urls")),

    path("services/", views.services_view, name="services"),

    path("gallery/", views.gallery_view, name="gallery"),

    path("contact/", views.contact_view, name="contact"),

    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),


    

]
