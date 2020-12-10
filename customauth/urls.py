from django.urls import path

from .views import current_user, UserList, UserContactsView

app_name = 'customauth'

urlpatterns = [
    path('current-user/', current_user),
    path('users/', UserList.as_view()),
    path('contacts/', UserContactsView.as_view()),
]
