from django.db import models
from django.urls import reverse
from datetime import date
# Create your models here.

WEATHER = (
    ('S', 'Sunny'),
    ('C', 'Cloudy'),
    ('R', 'Rainy'),
)

class Finch(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    def recent_sighting(self):
        print(self.sighting_set.filter(date=date.today()).count())
        print(self.sighting_set.filter())
        # return self.sighting_set.filter(date=date.today()) == self.sighting_set.filter('date').value()
        pass

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

class Armor(models.Model):
    style = models.CharField(max_length=50)
    material = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.finch.name} is ready for war in his {self.material}{self.style}"

    def get_absolute_url(self):
        return reverse('armor_detail', kwargs={'pk': self.id})

# class Weapon(models.Model):
#     style = models.CharField(max_length=50)
#     material = models.CharField(max_length=25)

#     def __str__(self):
#         return f"{self.finch.name} is ready for war in his {self.material}{self.style}"

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