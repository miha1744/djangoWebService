from django.shortcuts import render, redirect, get_object_or_404, reverse
from . import forms
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from .models import Event, Patient, Doctor, Service
from .utils import Calendar
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .forms import EventForm

#REST
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from . import serializers


# Create your views here.

#API Views

class RegisterAPIView(CreateAPIView):
    model = Patient
    permission_classes = [AllowAny]
    serializer_class = serializers.PatientSerializer



class GetDoctorsListAPIView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer


class GetAllPatients(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = serializers.PatientSerializer


class GetAllEvents(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.GetEventsSerializer



class UsersEvents(APIView):

    # def get_object(self, pk):
    #     try:
    #         return Event.objects.filter(doctor_id= pk)
    #     except Event.DoesNotExist:
    #         raise Http404

    def get(self, request):
        event = Event.objects.filter(patient__user=self.request.user)
        serializer = serializers.UsersEventsSerializer(event, many= True)
        return Response(serializer.data)



class GetEvent(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.filter(doctor_id= pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = serializers.GetEventsSerializer(event, many= True)
        return Response(serializer.data)


class CreateEventAPIView(CreateAPIView):
    model = Event
    serializer_class = serializers.CreateEventSerializer




class CreateDoctorView(CreateView):
    form_class = forms.DoctorRegisterForm
    success_url = reverse_lazy("login")
    template_name = "register.html"



class GetAllServices(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer



class GetPatients(APIView):

    def get(self, request):
        patient = Patient.objects.get(user=self.request.user)
        serializer = serializers.PatientSerializer(patient, many= False)
        return Response(serializer.data)




def accountSettings(request):
	doctor = request.user.doctor
	form = forms.DoctorEditForm(instance=doctor)

	if request.method == 'POST':
		form = forms.DoctorEditForm(request.POST, request.FILES,instance=doctor )
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'account_settings.html', context)




#Calendar
class CalendarView(LoginRequiredMixin ,generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user.id, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context




def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()


def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    instance = get_object_or_404(Event, pk=event_id)

    data = {"event": instance}
    return render(request, 'event.html', context= data)



class DailySheldue(LoginRequiredMixin ,generic.ListView):
    model = Event
    template_name = 'daily.html'


    def get_queryset(self):
        day =self.kwargs['day']
        month = self.kwargs['month']
        print(day, month)
        context = daily_view(day, month, self.request.user.id)

        return context


def get_real_date(req_day):
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day)
    return datetime.today()


def daily_view(day, month, id =1):
    events_per_day = Event.objects.filter(start_time__day=day, doctor__user_id=id, start_time__month=month)
    print(events_per_day)
    return events_per_day



