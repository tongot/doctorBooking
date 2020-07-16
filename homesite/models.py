from django.db import models

# Create your models here.
class WorkDone(models.Model):
    type_of_work = models.CharField(verbose_name='Type of work', max_length=200)
    amount_done = models.IntegerField(verbose_name='Work done')

    def __str__(self):
        return f'{self.type_of_work} {self.amount_done}'