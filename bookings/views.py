import razorpay
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from destinations.models import Destination
from .models import Booking


# ---------------- MY BOOKINGS ----------------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings
    })


# ---------------- BOOK DESTINATION ----------------
from datetime import datetime, date
from decimal import Decimal
from django.contrib import messages

@login_required
def book_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)

    if request.method == "POST":

        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        persons = int(request.POST.get("persons"))
        mobile_number = request.POST.get("mobile_number")

        # 🔥 CONVERT TO DATE
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        today = date.today()

        from bookings.models import Booking

        # 🔥 CHECK EXISTING BOOKINGS
        existing = Booking.objects.filter(
            destination=destination,
            start_date=start_date
        )

        total_booked = sum(b.persons for b in existing)

        # ❌ OVERBOOK CHECK
        if total_booked + persons > destination.capacity_per_day:
            messages.error(request, "Not enough slots available for selected date")
            return redirect("book_destination", destination_id=destination.id)

        # ❌ 1. Past date check
        if start_date < today:
            messages.error(request, "Start date must be in future")
            return redirect("book_destination", destination_id=destination.id)

        # ❌ 2. End before start
        if end_date < start_date:
            messages.error(request, "End date must be after start date")
            return redirect("book_destination", destination_id=destination.id)

        # ❌ 3. Season check (if exists)
        if destination.best_season_start and start_date < destination.best_season_start:
            messages.error(request, "Booking not allowed before season starts")
            return redirect("book_destination", destination_id=destination.id)

        if destination.best_season_end and end_date > destination.best_season_end:
            messages.error(request, "Booking exceeds season limit")
            return redirect("book_destination", destination_id=destination.id)

        # 💰 AMOUNT
        amount = Decimal(destination.price) * Decimal(persons)
        amount_paise = int(amount * 100)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        print("ORDER CREATED:", order)

        # 💾 STORE SESSION
        request.session['booking_data'] = {
            "destination_id": destination.id,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "persons": persons,
            "mobile_number": mobile_number,
            "amount": float(amount)
        }

        return render(request, "bookings/payment.html", {
            "destination": destination, 
            "order_id": order["id"],
            "amount_paise": amount_paise,
            "amount_rupees": amount,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    # 🔥 PASS DATES TO TEMPLATE
    return render(request, "bookings/book_destination.html", {
        "destination": destination,
        "today": date.today(),
        "season_start": destination.best_season_start,
        "season_end": destination.best_season_end
    })


# ---------------- RAZORPAY SUCCESS ----------------
import json
from django.http import JsonResponse

@login_required
def payment_success(request):

    if request.method == "POST":

        data = json.loads(request.body)

        # you can verify signature later (optional now)

        booking_data = request.session.get("booking_data")

        destination = Destination.objects.get(id=booking_data["destination_id"])

        Booking.objects.create(
            user=request.user,
            destination=destination,
            start_date=booking_data["start_date"],
            end_date=booking_data["end_date"],
            persons=booking_data["persons"],
            mobile_number=booking_data["mobile_number"],
            amount=booking_data["amount"],
            status="confirmed"
        )

        del request.session['booking_data']

        return JsonResponse({"status": "success"})

# ---------------- QR PAYMENT (MANUAL) ----------------
from django.core.mail import send_mail
from django.conf import settings

@login_required
def qr_payment_submit(request):

    data = request.session.get("booking_data")

    if not data:
        messages.error(request, "Session expired.")
        return redirect("dashboard")

    if request.method == "POST":
        screenshot = request.FILES.get("payment_screenshot")

        destination = Destination.objects.get(id=data["destination_id"])

        booking = Booking.objects.create(
            user=request.user,
            destination=destination,
            start_date=data["start_date"],
            end_date=data["end_date"],
            persons=data["persons"],
            mobile_number=data["mobile_number"],
            amount=data["amount"],
            payment_screenshot=screenshot,
            status="pending"
        )

        # 🔥 SEND PENDING EMAIL
        send_mail(
            subject="Booking Received - Trekora",
            message=f"""
            Hello {booking.user.username},

            Your booking request for {booking.destination.name} has been received.

            Status: PENDING APPROVAL

            Our admin team will verify your payment and confirm your booking soon.

            Details:
            Start Date: {booking.start_date}
            End Date: {booking.end_date}
            Persons: {booking.persons}

            Thank you for choosing Trekora!

            - Team Trekora
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.user.email],
            fail_silently=False,
        )

        del request.session['booking_data']

        messages.success(request, "Booking submitted! Waiting for admin approval.")
        return redirect("my_bookings")

# ---------------- CANCEL ----------------
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "cancelled":
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully.")

    return redirect("my_bookings")

@login_required
def payment_failed(request):
    messages.error(request, "Payment failed. Try again.")
    return redirect("dashboard")

from django.contrib.admin.views.decorators import staff_member_required

from destinations.models import Destination  # 🔥 ADD THIS AT TOP

def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    bookings = Booking.objects.all().order_by('-id')
    destinations = Destination.objects.all()   # 🔥 ADD THIS

    return render(request, "admin/dashboard.html", {
        "bookings": bookings,
        "destinations": destinations   # 🔥 ADD THIS
    })

@staff_member_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status != "pending":
        messages.error(request, "Action not allowed.")
        return redirect("admin_dashboard")

    booking.status = status
    booking.save()

    # 🔥 CONFIRMATION EMAIL
    if status == "confirmed":
        send_mail(
            subject="Booking Confirmed - Trekora",
            message=f"""
                Hello {booking.user.username},

                Your booking for {booking.destination.name} has been CONFIRMED.

                Details:
                Start Date: {booking.start_date}
                End Date: {booking.end_date}
                Persons: {booking.persons}

                We look forward to your adventure!

                - Team Trekora
                """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.user.email],
            fail_silently=False,
        )

    # 🔥 OPTIONAL: CANCEL EMAIL
    elif status == "cancelled":
        send_mail(
            subject="Booking Cancelled - Trekora",
            message=f"""
                Hello {booking.user.username},

                Your booking for {booking.destination.name} has been CANCELLED.

                If you have any questions, please contact us.

                - Team Trekora
                """,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[booking.user.email],
            fail_silently=False,
        )

    messages.success(request, f"Booking marked as {status}")
    return redirect("admin_dashboard")

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Review

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    review.delete()
    return redirect("profile")

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.rating = request.POST.get("rating")
        review.comment = request.POST.get("comment")
        review.save()

        return redirect("profile")

    return render(request, "bookings/edit_review.html", {
        "review": review
    })