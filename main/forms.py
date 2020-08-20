
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, CharField, DateInput
from . import models
from .models import Doctor, Event
from django import forms

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




class DoctorEditForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
