from django.shortcuts import render
from rest_framework import viewsets
from .serializers import NewsletterSerializer, CustomerSerializer, MessageSerializer
from notification.models import Newsletter, Message
from customer.models import Customer


class NewsletterView(viewsets.ModelViewSet):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
