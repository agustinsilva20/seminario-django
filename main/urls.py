
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
    path('crearcurso/', views.crearcurso, name='crearcurso'),
    path('joincurso/', views.joincurso, name='joincurso'),
    path('cursos/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('crearencuesta/<int:curso_id>/', views.crear_encuesta, name='crear_encuesta'),
    path('alumnos/<int:curso_id>/', views.alumnos, name='alumnos'),
    path('respuestasencuesta/<int:curso_id>/', views.respuestasencuesta, name='respuestasencuesta'),
    path('feedback/<int:curso_id>/', views.feedback, name='feedback'),
    path('responderencuesta/<int:curso_id>/', views.responderencuesta, name='responderencuesta')
    
]
# Maneja errores 404
