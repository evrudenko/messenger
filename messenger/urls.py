from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('users/', include('customauth.urls')),
    path('messages/', include('message.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
