from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.api.urls')),  # Include API URLs
]
