from django.db import models


class Post(models.Model):
    CASE_NUMBER = models.CharField(max_length=200)
    PREVAILING_WAGE = models.Text()
    PW_UNIT_OF_PAY = models.CharField(auto_now_add=True)
    TOTAL_SALARY=models.IntegerField()

    def __str__(self):
        return self.name

# Create your models here.
