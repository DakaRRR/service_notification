from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'newsletters', views.NewsletterView, basename='newsletter')
router.register(r'customers', views.CustomerView, basename='customer')
router.register(r'messages', views.MessageView, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

