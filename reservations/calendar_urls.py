from django.urls import path
from reservations.views import public_calendar, ical_feed

urlpatterns = [
    path('', public_calendar, name='public_calendar'),
    path('feed.ics', ical_feed, name='ical_feed'),
]
