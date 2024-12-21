from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Route(models.Model):
    start_city = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.start_city} to {self.destination}'
    

class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('single', 'Single Ride'),
        ('multiple', 'Multiple Rides'),
        ('pass', 'Pass (Weekly/Monthly)')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    route = models.CharField(max_length=255)  # Example: "Mumbai to Pune"
    status = models.CharField(max_length=20, default='Active')  # 'Active' or 'Used' or 'Expired'
    valid_until = models.DateTimeField(null=True, blank=True)  # If ticket is time-based
    generated_at = models.DateTimeField(auto_now_add=True)  # Time when ticket was booked
    
    def __str__(self):
        return f"{self.user.username} - {self.route} - {self.ticket_type}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.full_name

# Model for Saved Routes
class SavedRoute(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name="saved_routes", on_delete=models.CASCADE)
    route_name = models.CharField(max_length=100)

    def __str__(self):
        return self.route_name

# Model for Favorite Routes
class FavoriteRoute(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name="favorite_routes", on_delete=models.CASCADE)
    route_name = models.CharField(max_length=100)

    def __str__(self):
        return self.route_name

# Model for Notifications
class Notification(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name="notifications", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
