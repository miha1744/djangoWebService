from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.urls import reverse


from rest_framework.authtoken import views as auth_views

from . import views


api_urls = [
    path("api/v1/register", views.RegisterAPIView.as_view(), name="register"),
    path("api-token-auth", auth_views.obtain_auth_token, name="api-token-auth"),
    path("api/v1/doctors-list", views.GetDoctorsListAPIView.as_view(), name="doctors"),
    path("api/v1/events-list", views.GetAllEvents.as_view(), name="events"),
    path("api/v1/register-event", views.CreateEventAPIView.as_view(), name= "register-event"),
    path("api/v1/patients-list", views.GetAllPatients.as_view(), name ="patients-list")
]


web_urls = [
    path('',views.CalendarView.as_view(), name = 'home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', views.CreateDoctorView.as_view(), name="register-doctor"),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/new', views.event, name='event_new'),
    path('event/edit/<int:event_id>', views.event, name='edit'),
    path('daily/<int:day>/<int:month>',views.DailySheldue.as_view(), name ='daily'),
]


urlpatterns = web_urls + api_urls
