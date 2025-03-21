from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bitrix24/', include('web.apps.bitrix24.urls', namespace='bitrix24')),
]
