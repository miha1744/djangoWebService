from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.urls import reverse
from django.conf import settings
from rest_framework import  routers
from django.conf.urls.static import static


from rest_framework.authtoken import views as auth_views

from . import views


api_urls = [
    path("api/v1/register", views.RegisterAPIView.as_view(), name="register"),
    path("api-token-auth", auth_views.obtain_auth_token, name="api-token-auth"),
    path("api/v1/doctors-list", views.GetDoctorsListAPIView.as_view(), name="doctors"),
    path("api/v1/events-list", views.GetAllEvents.as_view(), name="events"),
    path("api/v1/register-event", views.CreateEventAPIView.as_view(), name= "register-event"),
    path("api/v1/patients-list", views.GetAllPatients.as_view(), name ="patients-list"),
    path("api/v1/events/<int:pk>", views.GetEvent.as_view(), name = "doctors_events"),
    path("api/v1/current_user_events", views.UsersEvents.as_view(), name = "current_user_events"),
    path("api/v1/services", views.GetAllServices.as_view(), name = "services"),
    path("api/v1/patient_info",views.GetPatients.as_view(), name = "current_user"),
    path("api/v1/coordinates",views.GetCoordinates.as_view(), name = "coordinates"),
    path("api/v1/timetable",views.GetTimetableListAPIView.as_view(), name = "timetableApi")
]


web_urls = [
    path('',views.CalendarView.as_view(), name = 'home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', views.CreateDoctorView.as_view(), name="register-doctor"),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/new', views.event, name='event_new'),


    #Timetable
    path('timetable', views.TimetableView.as_view(), name = 'timetable'),
    path('timetable_event/edit/<int:event_id>', views.timetable_event, name = 'timetable_edit'),
    path('timetable/new', views.timetable_event, name='timetable_new'),


    #Calendar
    path('event/edit/<int:event_id>', views.event, name='edit'),
    path('daily/<int:day>/<int:month>',views.DailySheldue.as_view(), name ='daily'),
    path('account/', views.accountSettings, name="account"),
]


urlpatterns = web_urls + api_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
