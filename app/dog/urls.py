from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dog import views

router = DefaultRouter()
router.register('dogs', views.DogViewSet)

app_name = 'dog'

urlpatterns = [
    path('', include(router.urls))
]
