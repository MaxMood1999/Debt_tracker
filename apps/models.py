from django.db import models
from django.db.models import CharField, DecimalField, BooleanField, DateTimeField


class Payment(models.Model):
    original_debt_id = models.IntegerField()
    contact_name = CharField(max_length=255)
    paid_amount = DecimalField(max_digits=10, decimal_places=2)
    payment_description = CharField(max_length=255)
    was_my_debt = BooleanField()
    payment_date = DateTimeField()

    def __str__(self):
        return f"{self.contact_name} - {self.paid_amount}"