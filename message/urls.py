from django.urls import path

from .views import UpdateDestroyMessageAPIView, ListCreateMessageAPIView

app_name = 'message'

urlpatterns = [
    path('messages/<int:pk>/', UpdateDestroyMessageAPIView.as_view()),
    path('messages/', ListCreateMessageAPIView.as_view()),
]
