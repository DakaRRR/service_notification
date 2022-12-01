from django.core.validators import RegexValidator
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    phone_regex = RegexValidator(regex=r'^7\d{10}$',
                                 message="Номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)")
    phone_number = models.CharField(validators=[phone_regex], unique=True, max_length=11)
    mobile_operator = models.CharField(max_length=5)
    tag = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Клиент {self.id} номер - {self.mobile_operator}{self.phone_number}'

    def get_phone_number(self):
        return self.mobile_operator + self.phone_number

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
