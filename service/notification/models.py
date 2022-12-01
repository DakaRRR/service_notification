from django.db import models

from django.db import models
from datetime import timezone
from customer.models import Customer


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Newsletter(BaseModel):
    text = models.TextField()
    mobile_operator = models.CharField(null=True, blank=True, default=None, max_length=5)
    tag = models.CharField(max_length=255, blank=True, default=None)
    date_send_from = models.DateTimeField()
    date_send_to = models.DateTimeField()

    def to_send(self):
        now = timezone.now()
        if self.date_send_to <= now <= self.date_send_from:
            return True
        else:
            return False

    def __str__(self):
        return f'Рассылка {self.id} с {self.date_send_from} текст - {self.text}'

    class Meta:
        verbose_name = 'newsletter'
        verbose_name_plural = 'newsletters'
        ordering = ('date_send_to',)


class Message(BaseModel):
    class Status(models.IntegerChoices):
        sent = 1, "Отправлено"
        not_sent = 0, "Не отправлено"

    date_sent = models.DateTimeField()
    status = models.PositiveSmallIntegerField(verbose_name="Статус отправки", choices=Status.choices,
                                              default=Status.not_sent)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.SET_DEFAULT, default="Рассылка удалена")

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'Сообщение {self.id} рассылки {self.newsletter} для {self.customer}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('date_sent',)
