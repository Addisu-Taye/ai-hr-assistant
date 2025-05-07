from django.contrib import admin
from django.urls import path, include  # Add 'include' to the import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hr_data/', include('data_management.urls')),
    path('analytics/', include('analytics.urls')),
    ]