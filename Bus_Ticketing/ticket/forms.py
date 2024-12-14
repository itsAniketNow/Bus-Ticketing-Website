from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'phone_number', 'profile_image']

class NotificationForm(forms.Form):
    # For clearing notifications (you can adjust as needed)
    clear_notifications = forms.BooleanField(required=False)
