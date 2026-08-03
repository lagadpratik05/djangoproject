
Detailed Key Features
User Authentication & Authorization: Full registration, login, session management, and custom user profiles.  
Trek & Destination Management: Browse trek listings with duration, difficulty, best seasonal times, and dynamic pricing.  
Interactive Booking Workflow: Select start/end dates, specify headcount, pay via custom QR payment integration, and upload proof of payment screenshots.  
User Dashboard: View booking statuses (Pending/Confirmed/Cancelled) with real-time cancellation options.  
Responsive UI/UX: Styled using Tailwind CSS with glassmorphism components, scroll animations, and Lucide icons.  
2. 📁 Extended Project Directory Structure
core/
├── accounts/               # User authentication, profiles, views & logic[span_9](start_span)[span_9](end_span)
│   ├── templates/          # Login, Signup, and Profile pages[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span)
│   └── views.py            # Profile, Contact, Gallery, and Service handlers[span_12](start_span)[span_12](end_span)
├── bookings/               # Trek booking system & logic[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span)[span_15](start_span)[span_15](end_span)
│   ├── templates/          # Booking form, booking history, and cancel view[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span)
│   └── urls.py             # Route definitions for booking management[span_18](start_span)[span_18](end_span)
├── core/                   # Project configurations and settings
│   ├── settings.py         # Main Django settings
│   └── urls.py             # Root URL routing[span_19](start_span)[span_19](end_span)
├── static/                 # Static assets[span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span)[span_23](start_span)[span_23](end_span)
│   ├── css/                # Custom stylesheets[span_24](start_span)[span_24](end_span)
│   ├── images/             # QR codes, brand logos, favicons[span_25](start_span)[span_25](end_span)[span_26](start_span)[span_26](end_span)[span_27](start_span)[span_27](end_span)[span_28](start_span)[span_28](end_span)
│   └── js/                 # Reveal animations & UI logic[span_29](start_span)[span_29](end_span)[span_30](start_span)[span_30](end_span)[span_31](start_span)[span_31](end_span)
├── db.sqlite3              # Database
└── manage.py               # Django entry point[span_32](start_span)[span_32](end_span)

. 🌐 API & URL Routes Overview
RouteView / FunctionDescription
/login/login_viewUser login portal
/signup/signup_viewNew user registration
/dashboard/dashboardUser dashboard landing page
/profile/profile_viewUser profile page
/services/views.services_viewServices provided page
/gallery/views.gallery_viewPhoto gallery showcase
/contact/views.contact_viewCustomer contact form
/privacy/views.privacyPrivacy policy document
/terms/views.termsTerms & conditions document

HOW TO RUN PROJECT...

Step 1: Open Command Prompt in Your Project Directory
Downloads > Project - Copy (2) > Project > nisargpath_django > core

Click on the address bar at the top, type cmd, and press Enter.

Step 2: Set Up & Activate Virtual Environment
Your project already has a .venv folder (located one directory up inside nisargpath_django). Activate it by running:
..\.venv\Scripts\activate

Step 3: Install Requirements
Ensure Django and required dependencies are installed:pip install django pillow

Step 4: Apply Database Migrations
Run these commands to prepare your SQLite database
python manage.py makemigrations
python manage.py migrate

Step 5: Start the Development Server
Launch the Django local web server:
python manage.py runserver
