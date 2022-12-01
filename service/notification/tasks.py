from datetime import timezone
from service_project.celery import app
from notification.models import Newsletter, Message
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


def send_message(message, text, phone_number, end_date):
    new_message = {
        "id": message.id,
        "phone": str(phone_number),
        "text": text
    }
    headers = {
        "Authorization": TOKEN,
        'Content-Type': 'application/json'}
    if timezone.now < end_date:
        try:
            request = requests.post(f"{BASE_URL}/{message.id}", json=new_message, headers=headers)
        except request.exceptions.RequestException as exc:
            logger.error(f"При отправке сообщения: {message.id} возникла ошибка {exc}")
        else:
            logger.info(f"Cообщение : {message.id}, Статус отправки: 'Отправлено'")
            message.update(sending_status='Sent')


def prepare_message(newsletter_id: int):
    'Подготовка отправки сообщения, создание рассылки и клиентов по каждому из базы отправляем сообщение'
    newsletter = Newsletter.objects.get(id=newsletter_id)
    customers = get_customers(newsletter.tag, newsletter.mobile_operator)
    for customer in customers:
        message = Message.objects.create(date_sent=timezone.now(),
                                         newsletter_id=newsletter_id,
                                         customer_id=customer.id)
        logger.info(f'Сообщение {message.id} {newsletter.text} отправляется клиенту {customer.mobile_operator}')

        send_message(message=message, text=newsletter.text, phone_number=customer.phone_number)


def to_send(newsletter):
    now = timezone.now()
    if newsletter.date_send_to <= now <= newsletter.date_send_from:
        return True
    else:
        return False


@app.task
def check_send():
    "Проверяет есть ли раасылки которые надо отправить"
    newsletters = Newsletter.objects.all()
    for newsletter in newsletters:
        if to_send(newsletter):
            prepare_message(newsletters.id)
        else:
            logger.info("Ничего отправлять не надо...")




