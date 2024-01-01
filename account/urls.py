from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('hello/',views.hello_world,name="hi"),
    path('',views.CreateProfileListView.as_view(),name="Create-profile"),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/',views.CookieTokenRefreshView.as_view(),name='token_refresh'),
    path('logout/',views.logoutView,name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
