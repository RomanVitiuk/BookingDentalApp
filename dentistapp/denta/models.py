from django.db import models
from .utils import DOC_GRADE


class DentistDoctor(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=100)
    edication_grade = models.CharField(
        max_length=8, choices=DOC_GRADE, default=DOC_GRADE[0]
    )
    experience = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Client(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    doc = models.ForeignKey(DentistDoctor, on_delete=models.PROTECT)
    visit_date = models.DateTimeField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
