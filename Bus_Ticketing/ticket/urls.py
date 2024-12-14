from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('live-tracking/', views.live_tracking, name='live_tracking'),
    path('user_account/', views.user_account, name='user_account'),
    path('timetables/', views.timetables, name='timetables'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout_message/', views.logout_message, name='logout_message'),
    path('signup/', views.signup, name='signup'),
    path('book-ticket/<int:route_id>/', views.ticket_booking, name='book_ticket'),
    # path('ticket_booking/', views.ticket_booking, name='ticket_booking'),
    path('active_tickets/', views.active_tickets, name='active_tickets'),
    path('ticket_history/', views.ticket_history, name='ticket_history'),
]