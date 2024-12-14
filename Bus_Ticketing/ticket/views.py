from django.shortcuts import render, redirect, get_object_or_404
from .models import Route, Ticket
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, SavedRoute, FavoriteRoute, Notification
from .forms import UserProfileForm, NotificationForm
from django.utils import timezone
from django.http import JsonResponse
# import qrcode  # To generate QR codes
import json

# Create your views here.

# View for the homepage
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
# View for searching routes
def search_routes(request):
    # Querying the routes
    routes = Route.objects.all().values('pk', 'start_city', 'destination', 'price')
    
    # Convert Decimal to float for JSON serialization
    for route in routes:
        route['price'] = float(route['price'])  # Convert Decimal to float

    # Serialize the data
    routes_json = json.dumps(list(routes))
    
    return render(request, 'route_search.html', {
        'routes_json': routes_json
    })

# View for live tracking
def live_tracking(request):
    return render(request, 'live_tracking.html')

# View for timetables
def timetables(request):
    return render(request, 'timetables.html')


# View for login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("login")
        password = request.POST.get("login-password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("home")  # Redirect to the homepage after login
        else:
            messages.error(request, "Invalid username or password")
            return redirect("signup")

    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate if the email is already used
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'signup.html')

        # Create a new user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        messages.success(request, "Signup successful! Please log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'signup.html')  # Render the signup page for GET requests

@login_required
# View for ticket booking
def ticket_booking(request, route_id    ):
    route = get_object_or_404(Route, pk=route_id)  # Get the selected route
    
    if request.method == 'POST':
        # Get data from the form
        ticket_type = request.POST.get('ticketType')
        
        # Create a new ticket for the logged-in user
        new_ticket = Ticket.objects.create(
            user=request.user,
            ticket_type=ticket_type,
            route=route,
            valid_until=timezone.now() + timezone.timedelta(hours=2),  # Example of valid time
            status='Active'  # Set the ticket status to 'Active' initially
        )
        
        return redirect('active_tickets')  # Redirect to the active tickets page

    return render(request, 'ticket_booking.html', {'route_id': route_id}    )

@login_required
# View for active tickets
def active_tickets(request):
    tickets = Ticket.objects.filter(user=request.user, status='Active')
    return render(request, 'active_tickets.html', {'tickets': tickets})

@login_required
# View for ticket history
def ticket_history(request):
    tickets = Ticket.objects.filter(user=request.user).exclude(status='Active')
    return render(request, 'ticket_history.html', {'tickets': tickets})


# View for User Account (Profile, Routes, Notifications)
@login_required
def user_account(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # If the user submits an updated profile
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_account')
    else:
        profile_form = UserProfileForm(instance=user_profile)

    # Get saved routes and favorite routes
    saved_routes = SavedRoute.objects.filter(user_profile=user_profile)
    favorite_routes = FavoriteRoute.objects.filter(user_profile=user_profile)

    # Handle notifications
    notifications = Notification.objects.filter(user_profile=user_profile)
    
    # Handling the clear notifications functionality
    if request.method == 'POST' and 'clear_notifications' in request.POST:
        Notification.objects.filter(user_profile=user_profile).update(is_read=True)

    return render(request, 'user_account.html', {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'saved_routes': saved_routes,
        'favorite_routes': favorite_routes,
        'notifications': notifications,
    })

# Logout view
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('logout_message')  # Redirect to the logout message page

def logout_message(request):
    return render(request, 'logout_message.html')