
from django.urls import path
from . import views
from .views import OAuthCallbackView, OAuthRedirectView



urlpatterns = [
    path("", views.index, name="index"),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('admin/', views.admin, name='admin'),
    path('oauth-redirect/', OAuthRedirectView.as_view(), name='oauth_redirect'),
    path('oauth-callback/', OAuthCallbackView.as_view(), name='oauth_callback'),
    
]
# Maneja errores 404
