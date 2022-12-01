import time

from decouple import config
from django.db.models import Q
from .models import Newsletter, Message
from customer.models import Customer
from celery.utils.log import get_task_logger

from django.utils import timezone
import requests

BASE_URL = config(str('BASE_URL'))
TOKEN = config(str('TOKEN'))

logger = get_task_logger(__name__)


def get_customers(tag, mobile_operator):
    customers = Customer.objects.filter(
        Q(mobile_operator=mobile_operator) |
        Q(tag=tag)
    )
    return customers


def send_message(message, text, phone_number):
    new_message = {
        "id": message.id,
        "phone": str(phone_number),
        "text": text
    }
    headers = {
        "Authorization": TOKEN,
        'Content-Type': 'application/json'}

    try:
        request = requests.post(f"{BASE_URL}/{message.id}", json=new_message, headers=headers)
    except request.exceptions.RequestException as exc:
        logger.error(f"При отправке сообщения: {message.id} возникла ошибка {exc}")
    else:
        logger.info(f"Cообщение : {message.id}, Статус отправки: 'Отправлено'")
        message.update(sending_status='Sent')


def prepare_message(newsletter_id: int):
    'Подготовка отправки сообщения, создание рассылки и клиентов по каждому клиенту из базы отправляем сообщение'
    newsletter = Newsletter.objects.get(id=newsletter_id)
    customers = get_customers(newsletter.tag, newsletter.mobile_operator)
    for customer in customers:
        message = Message.objects.create(date_sent=timezone.now(),
                                         newsletter_id=newsletter_id,
                                         customer_id=customer.id)
        print(f'Сообщение {message.id} {newsletter.text} отпраялется клиенту {customer.mobile_operator}')

        send_message(message=message, text=newsletter.text, phone_number=customer.phone_number)



