from django.db import models

class Nutrition(models.Model):
    calories = models.FloatField()
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)