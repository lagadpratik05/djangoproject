from django.shortcuts import render
from .models import Destination
from bookings.models import Review   # 🔥 add this
from django.db.models import Avg     # 🔥 add this
import requests

from django.db.models import Avg
from bookings.models import Review
from django.db.models import Case, When, IntegerField

from django.db.models import Case, When, IntegerField, Avg
from datetime import date
from bookings.models import Review

def destinations_list(request):

    destinations = Destination.objects.annotate(
        priority=Case(
            When(status="available", then=0),
            When(status="unavailable", then=1),
            default=2,
            output_field=IntegerField(),
        )
    ).order_by("priority")

    today = date.today()   # 🔥 ADD THIS

    for d in destinations:

        # =========================
        # 🔥 ADD THIS BLOCK HERE
        # =========================
        if d.best_season_start and d.best_season_end:
            d.is_available = d.best_season_start <= today <= d.best_season_end
        else:
            d.is_available = True
        # =========================

        # ⭐ EXISTING RATING LOGIC
        avg = Review.objects.filter(destination_id=d.id).aggregate(Avg('rating'))
        d.avg_rating = avg['rating__avg'] or 0

        print("DEBUG:", d.name, "->", d.avg_rating, "| Available:", d.is_available)

    return render(request, "destinations/destinations.html", {
        "destinations": destinations
    })

from django.shortcuts import get_object_or_404

from django.shortcuts import render, get_object_or_404
from .models import Destination
def destination_detail(request, pk):
    destination = get_object_or_404(Destination, id=pk)

    # 🔥 GET REVIEWS
    reviews = Review.objects.filter(destination=destination).order_by('-id')

    # 🔥 AVERAGE RATING
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # 🔥 HANDLE REVIEW SUBMIT
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not Review.objects.filter(user=request.user, destination=destination).exists():
            Review.objects.create(
                user=request.user,
                destination=destination,
                rating=rating,
                comment=comment
            )

        return redirect("destination_detail", pk=pk)

    # 🔥 WEATHER API
    api_key = "85f0d096f71ea4c30d82413de2f3b850"
    city = destination.location

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        temperature = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]

    except:
        temperature = "N/A"
        weather_desc = "Unavailable"

    # ✅ SINGLE RETURN (IMPORTANT)
    return render(request, "destinations/destination_detail.html", {
        "destination": destination,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
        "temperature": temperature,
        "weather_desc": weather_desc,
    })

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Destination


@staff_member_required
def add_destination(request):

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        Destination.objects.create(
            name=name,
            price=price,
            image=image,
            status="available"
        )

        messages.success(request, "Destination added successfully")
        return redirect("admin_dashboard")

    return render(request, "admin/add_destination.html")

@staff_member_required
def edit_destination(request, id):

    destination = get_object_or_404(Destination, id=id)

    if request.method == "POST":
        destination.name = request.POST.get("name")
        destination.price = request.POST.get("price")

        if request.FILES.get("image"):
            destination.image = request.FILES.get("image")

        destination.save()

        messages.success(request, "Destination updated")
        return redirect("admin_dashboard")

    return render(request, "admin/edit_destination.html", {
        "destination": destination
    })

@staff_member_required
def delete_destination(request, id):
    destination = get_object_or_404(Destination, id=id)
    destination.delete()

    messages.success(request, "Destination deleted")
    return redirect("admin_dashboard")