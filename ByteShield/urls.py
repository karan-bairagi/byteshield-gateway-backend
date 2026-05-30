"""
URL configuration for ByteShield project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import InactiveView,AllAPIKey,DeleteAPIView,ExternalTrafficChechView
from api.views import Signup,Login,GenerateAPIKey,SecurityScannerCharts,SecurityScannerDashboard,UserprofileUpdate
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/signup/',Signup.as_view()),
    path('api/v1/auth/login/',Login.as_view()),
    path('api/v1/api-keys/',GenerateAPIKey.as_view()),
    path('api/v1/user/profile/',SecurityScannerDashboard.as_view()),
    path('api/v1/dashboard/metrics/',SecurityScannerCharts.as_view()),
    path('api/v1/dashboard/charts/',UserprofileUpdate.as_view()),
    path('api/v1/api_key/inactive/',InactiveView.as_view()),
    path('api/v1/api_key/all/',AllAPIKey.as_view()),
    path('api/v1/api_key/delete/',DeleteAPIView.as_view()),
    path('api/v1/auth/token/refresh/',TokenRefreshView.as_view()),
    # Client API Traffic Logger Gateway
    path('api/v1/shield/verify/',ExternalTrafficChechView.as_view()),
]
