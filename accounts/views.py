from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from destinations.models import Destination
from django.contrib import messages



def login_view(request):
    context = {}

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            context["email_error"] = "Email and password are required"
        else:
            user = authenticate(
                request,
                username=email,   # email IS username
                password=password
            )

            if user is not None:
                login(request, user)

                # 🔥 ROLE BASED REDIRECT
                if user.is_staff:
                    return redirect("admin_dashboard")
                else:
                    return redirect("dashboard")
            else:
                context["password_error"] = "Invalid email or password"

    return render(request, "accounts/login.html", context)


from django.contrib.auth.models import User
from django.contrib.auth import login

def signup_view(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        # Validation
        if not name:
            context["name_error"] = "Name is required"
        elif not email:
            context["email_error"] = "Email is required"
        elif User.objects.filter(username=email).exists():
            context["email_error"] = "Email already registered"
        elif not password or len(password) < 6:
            context["password_error"] = "Password must be at least 6 characters"
        else:
            # Create user safely
            user = User.objects.create_user(
                username=email,   # email as username (important)
                email=email,
                password=password
            )

            # OPTIONAL but recommended: auto-login after signup
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("dashboard")

    return render(request, "accounts/signup.html", context)

from destinations.models import Destination
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    featured_destinations = Destination.objects.filter(
        status="available"
    ).order_by("-created_at")[:6]

    return render(request, "accounts/dashboard.html", {
        "featured_destinations": featured_destinations
    })


def logout_view(request):
    logout(request)
    return redirect("login")


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bookings.models import Booking


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bookings.models import Booking, Review

from accounts.models import Profile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        new_username = request.POST.get("username", "").strip()
        new_email = request.POST.get("email", "").strip().lower()
        new_image = request.FILES.get("image")

        updated = False  # track changes

        # 🔹 USERNAME CHANGE
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, "Username already taken")
                return redirect("profile")
            user.username = new_username
            updated = True

        # 🔹 EMAIL CHANGE
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, "Email already exists")
                return redirect("profile")
            user.email = new_email
            updated = True

        # 🔹 PROFILE IMAGE
        profile, created = Profile.objects.get_or_create(user=user)

        if new_image:
            profile.image = new_image
            profile.save()
            updated = True

        # 🔹 REMOVE IMAGE
        if "remove_image" in request.POST:
            profile.image = None
            profile.save()
            updated = True

        # 🔹 SAVE ONLY IF CHANGED
        if updated:
            user.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.warning(request, "No changes made")

        return redirect("profile")

    return render(request, "accounts/profile.html")

def services_view(request):
    return render(request, "accounts/services.html")


def gallery_view(request):
    gallery_images = [
        {
            "src": "https://tse2.mm.bing.net/th/id/OIP.S0F9fFQRoqd4VyuRR6q8iAHaE9",
            "alt": "Rajgad Fort Trek",
            "location": "Maharashtra - Pune",
        },
        {
            "src": "https://nomadsofindia.com/wp-content/uploads/2023/04/Kalsubai-Trek-2.jpg",
            "alt": "Kalsubai Peak",
            "location": "Maharashtra - Highest Peak",
        },
        {
            "src": "https://harishchandragad.in/wp-content/uploads/2022/04/IMG_20201029_114832-scaled.jpg",
            "alt": "Harishchandragad Trek",
            "location": "Maharashtra - Ahmednagar",
        },
        {
            "src": "https://www.holidify.com/images/bgImages/RAJMACHI.jpg",
            "alt": "Rajmachi Fort",
            "location": "Maharashtra - Lonavala",
        },
        {
            "src": "https://tse2.mm.bing.net/th/id/OIP.o7IOpWYcTexStqlegb0h5wHaEc",
            "alt": "Sahyadri Mountain Range",
            "location": "Maharashtra - Western Ghats",
        },
        {
            "src": "https://pbs.twimg.com/media/FDKAXTOVQAQOZOn.jpg",
            "alt": "Monsoon Treks",
            "location": "Maharashtra - Raigad",
        },
    ]

    return render(request, "accounts/gallery.html", {
        "gallery_images": gallery_images
    })


from django.contrib import messages
from django.shortcuts import render

def contact_view(request):
    if request.method == "POST":
        # You can later add send_mail() here
        messages.success(request, "Message sent successfully! We'll get back to you soon.")

    return render(request, "accounts/contact.html")




def destinations_view(request):
    destinations = Destination.objects.all()
    return render(request, "destinations/destinations.html", {
        "destinations": destinations
    })

from django.shortcuts import render

def privacy(request):
    return render(request, "privacy.html")

def terms(request):
    return render(request, "terms.html")
