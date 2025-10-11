from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 👇 Homepage API view with environment info
def home(request):
    environment = "development" if settings.DEBUG else "production"

    data = {
        "project": "IgniteEra Backend API",
        "message": "Welcome to IgniteEra Backend API 🚀",
        "status": "success",
        "environment": environment,
        "endpoints": {
            "admin": "/admin/",
            "api_root": "/api/",
            "auth_login_logout": "/api/auth/",
            "auth_registration": "/api/auth/registration/",
            "token_obtain": "/api/token/",
            "token_refresh": "/api/token/refresh/",
        },
        "credits": "Developed by IgniteEra Team ⚡"
    }
    return JsonResponse(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # replace 'core' with your app name if different
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),

    # 👇 Homepage (root URL)
    path('', home),
]
