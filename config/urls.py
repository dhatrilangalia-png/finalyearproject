from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('meetings/', include('apps.meetings.urls')),
    path('email/', include('apps.email_ai.urls')),
]
