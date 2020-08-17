
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.





class Doctor(models.Model):
    # relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # basic information
    name = models.CharField(max_length=50, help_text="Name of a doctor")

    profession = models.CharField(max_length=50, help_text="Profession of a doctor")

    image = models.ImageField(default= "NoneImage.jpg",null=True, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"


class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, help_text="Name of a user")

    def __str__(self):
        return f"{self.name}"



class Event(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, blank=True, related_name='patient')
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, blank=True, related_name='doctors')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    @property
    def get_html_url(self):
        url = reverse('edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


    @property
    def get_daily_url(self):
        url = reverse('daily', args=(self.start_time.day, self.start_time.month))
        return url



