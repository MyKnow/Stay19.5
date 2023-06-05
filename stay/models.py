from django.db import models
import datetime

# Create your models here.
from django.db import models

class Stay_model(models.Model):
    input_time = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    people_1 = models.JSONField(null=True)
    people_2 = models.JSONField(null=True)
    people_3 = models.JSONField(null=True)
    people_4 = models.JSONField(null=True)
    people_5 = models.JSONField(null=True)
    people_6 = models.JSONField(null=True)
    people_1_val = models.CharField(max_length=255, null=True)
    people_2_val = models.CharField(max_length=255, null=True)
    people_3_val = models.CharField(max_length=255, null=True)
    people_4_val = models.CharField(max_length=255, null=True)
    people_5_val = models.CharField(max_length=255, null=True)
    people_6_val = models.CharField(max_length=255, null=True)



    class Meta:
        db_table = 'real_final_stay2'
