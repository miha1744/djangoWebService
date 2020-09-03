from rest_framework import serializers
from django.forms import ModelForm, EmailField, CharField, DateInput
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from . import models

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password")




class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)

    class Meta:
        model = models.Patient
        fields = ("pk", "name", "user")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        patient = models.Patient.objects.create(
            name=validated_data["name"], user=user
        )
        return patient


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Doctor
        fields = ("pk", "name", "profession", "image")


    # doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, blank=True)
    # title = models.CharField(max_length=200)
    # description = models.TextField()
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField()


class GetEventsSerializer(serializers.ModelSerializer):

    doctor = serializers.SlugRelatedField(write_only=False, slug_field='pk', queryset = models.Doctor.objects.all())

    class Meta:
        model = models.Event
        fields = ("doctor", "title", "description", "start_time")


class UsersEventsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    doctor = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = models.Event
        fields = ("title", "description", "start_time","doctor", "user")


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coordinates
        fields = ("latitude", "longitude")




class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ("title", "description")


class CreateEventSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(write_only=True, slug_field='pk', queryset = models.Doctor.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    def create(self, validated_data):
        user = validated_data.pop("user")
        patient = models.Patient.objects.get(user=user) # тут находишь пациента по юзеру
        return models.Event.objects.create(patient = patient, **validated_data)

    class Meta:
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%y %H:%M'),
        }
        model = models.Event
        fields = ("user","doctor", "title", "description", "start_time")


