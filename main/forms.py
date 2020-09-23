

import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, CharField, DateInput
from . import models
from .models import Doctor, Event, Timetable
from django import forms


from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


class DoctorRegisterForm(UserCreationForm):

    email = EmailField(label="Email")
    full_name = CharField(max_length=60)
    specialization = CharField(max_length=60)

    class Meta:
        model = User
        fields = ("username", "email", "full_name", "specialization")

    def save(self, commit=True):
        user = super(DoctorRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        doctor = models.Doctor.objects.create(
            user=user,
            name=self.cleaned_data["full_name"],
            profession=self.cleaned_data["specialization"],
        )
        doctor.save()
        return user


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%y %H:%M'),
        }
        fields = '__all__'



class TimetableForm(ModelForm):

    def create(self, validated_data):
        user = validated_data.pop("user")
        doctor = models.Doctor.objects.get(user=user) # тут находишь пациента по юзеру
        return models.Timetable.objects.create(doctor = doctor, **validated_data)


    class Meta:
        model = Timetable
        # datetime-local is a HTML5 input type, format to make date time show on fields
        fields = ['doctor','day','start_time']
        widgets = {
            'day': DatePickerInput( options={
                    "format": "DD.MM.YYYY", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                    "minDate": str(datetime.datetime.now()),
                } ),
            'start_time': TimePickerInput(),
            'doctor': forms.HiddenInput()
        }






class DoctorEditForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
