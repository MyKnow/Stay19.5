from django.db import models

# Create your models here.
from django.db import models

class Stay_model(models.Model):
    id_token = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    people_num1 = models.IntegerField(null=True)
    people_num2 = models.IntegerField(null=True)
    people_num3 = models.IntegerField(null=True)
    people_num4 = models.IntegerField(null=True)
    people_num5 = models.IntegerField(null=True)
    people_num6 = models.IntegerField(null=True)
    people_num7 = models.IntegerField(null=True)
    people_num8 = models.IntegerField(null=True)
    people_num9 = models.IntegerField(null=True)
    people_num10 = models.IntegerField(null=True)
    people_num11 = models.IntegerField(null=True)
    people_num12 = models.IntegerField(null=True)
    people_num13 = models.IntegerField(null=True)
    people_num14 = models.IntegerField(null=True)
    people_num15 = models.IntegerField(null=True)
    people_num16 = models.IntegerField(null=True)
    people_num17 = models.IntegerField(null=True)
    people_num18 = models.IntegerField(null=True)
    people_num19 = models.IntegerField(null=True)
    people_num20 = models.IntegerField(null=True)

    class Meta:
        db_table = 'stay_table'
