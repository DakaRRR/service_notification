from rest_framework import serializers
from notification.models import Newsletter, Message
from customer.models import Customer


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('id', 'text', 'tag', 'date_send_from', 'date_send_to')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'phone_number', 'mobile_operator', 'tag')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'