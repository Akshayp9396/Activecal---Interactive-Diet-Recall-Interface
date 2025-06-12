from django.db import models

# Create your models here.

from django.db import models

from django.db import models

class Food(models.Model):
    food_code = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)

    def __str__(self):
        return self.description
