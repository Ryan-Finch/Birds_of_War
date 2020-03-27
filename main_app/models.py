from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

WEATHER = (
    ('S', 'Sunny'),
    ('C', 'Cloudy'),
    ('R', 'Rainy'),
)


class Armor(models.Model):
    style = models.CharField(max_length=50)
    material = models.CharField(max_length=25)

    def __str__(self):
        return f"Ready for war with {self.material}{self.style}"

    def get_absolute_url(self):
        return reverse('armor_detail', kwargs={'pk': self.id})

class Finch(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    armor = models.ManyToManyField(Armor)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def recent_sighting(self):
        sighting = self.sighting_set.filter(date=date.today()).count()
        
        if sighting == 1:
            return sighting
        elif sighting > 1:
            return sighting
    
    

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

class Sighting(models.Model):
    date = models.DateField('sighting date')
    weather = models.CharField(
        max_length=1,
        choices=WEATHER,
        default=WEATHER[0][0],
    )

    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_weather_display()} on {self.date}"

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __Str_(self):
        return f'Photo for finch_id:{self.finch_id} @{self.url}'