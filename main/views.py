from django.shortcuts import render, redirect
from .decorators import login_obligatorio
from .querys import sql_obtener_cuenta_by_nombre, sql_obtener_cuenta_by_mail, sql_obtener_cuenta_by_hash, sql_insert_hash,sql_crear_cuenta,select_all
from django.http import HttpResponse
from django.views import View
import string
import random

def logout(request):
    response = redirect('home')
    response.delete_cookie('pure_valorant_token')
    return response


def admin(request):
    resultados = select_all()
    dto = {"resultados":resultados }
    return render(request, "admin.html",dto)


@login_obligatorio
def home(request):
    query = sql_obtener_cuenta_by_hash(request.COOKIES.get('pure_valorant_token'))
    dto = {"riot_token": "",}
    try:
        riot_token = query[0][5]
        if riot_token is None:
            dto ["riot_token"] =  "Necesitas vincular tu cuenta de Riot con Pure Valorant: Haz click para continuar"
        return render(request, 'home.html',dto)
    except:
        return redirect('login')


def index(request):
    return render(request, 'landingpage.html')

def login(request):
    dto = {"mensaje":"",
           "valor_user":"",
            "valor_password1":"",
            }
    if request.method == 'GET':
        return render(request, 'login.html',dto)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Verificar si el usuario ya existe
        user_query = sql_obtener_cuenta_by_nombre(username)
        if len(user_query) == 0:
            dto["mensaje"] = "La cuenta no existe"
            dto["valor_user"] = username
            dto["valor_password1"] = password
            return render(request, 'login.html',dto)
        # Verifico si la password es incorrecta
        if user_query[0][2] != password:
            dto["mensaje"] = "La contraseña es incorrecta"
            dto["valor_user"] = username
            dto["valor_password1"] = password
            return render(request, 'login.html',dto)
        # Creo un hash de 30 caracteres
        hashValido = False
        while not hashValido:
            caracteres = string.ascii_letters + string.digits
            longitud = 30
            hash = ''.join(random.choice(caracteres) for i in range(longitud))
            # Verifico que el hash no exista en la base de datos
            hash_query = sql_obtener_cuenta_by_hash(hash)
            if len(hash_query) == 0:
                # Inserto el hash en la base de datos
                sql_insert_hash(hash, username)
                hashValido = True
                # Guardo el hash en una cookie
                # Establece la cookie
                response = redirect('home')
                response.set_cookie('pure_valorant_token', hash, max_age=3600) # Duración en segundos (1 hora)


        # Redirijo al usuario
        return response
def registro(request):
    if request.method == 'GET':
        dto = {"correoMensaje":"",
               "passwordMensaje":"",
               "usernameMensaje":"",
               "valor_user":"",
               "valor_email":"",
               "valor_password1":"",
               "valor_password2":"",
               }
        return render(request, "registro.html", dto)
    
    elif request.method == 'POST':
        # Accede a los datos del formulario
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        username = request.POST.get('username')

        # Dto a enviar si hay un error
        dto_error = {"correoMensaje":"",
               "passwordMensaje":"",
               "usernameMensaje":"",
               "valor_user":"",
               "valor_email":"",
               "valor_password1":"",
               "valor_password2":"",
               }

        # Si las contraseñas no coinciden
        if password != confirmPassword:
            dto_error["passwordMensaje"] = "Las contraseñas no coinciden"
            dto_error["valor_user"] = username
            dto_error["valor_email"] = email
            dto_error["valor_password1"] = password
            dto_error["valor_password2"] = confirmPassword

            return render(request, "registro.html", dto_error)
        
        # Verificar si el usuario ya existe
        user_query = sql_obtener_cuenta_by_nombre(username)
        if len(user_query) > 0:
            # Si el usuario ya existe
            dto_error["usernameMensaje"] = "El usuario ya se encuentra registrado"
            dto_error["valor_user"] = username
            dto_error["valor_email"] = email
            dto_error["valor_password1"] = password
            dto_error["valor_password2"] = confirmPassword
            return render(request, "registro.html", dto_error)

        # Verificar si el mail ya esta registrado
        mail_query = sql_obtener_cuenta_by_mail(email)
        if len(mail_query) > 0:
            # Si el mail ya existe
            dto_error["correoMensaje"] = "El correo electronico ya se encuentra registrado"
            dto_error["valor_user"] = username
            dto_error["valor_email"] = email
            dto_error["valor_password1"] = password
            dto_error["valor_password2"] = confirmPassword
            return render(request, "registro.html", dto_error)
        
        # Si no hay problemas registro la cuenta
        sql_crear_cuenta(username,password, email)
        return render(request, "registro_exito.html", dto_error)

class OAuthRedirectView(View):
    def get(self, request, *args, **kwargs):
        # URL de redirección a OAuth
        oauth_redirect_url = "https://auth.riotgames.com/authorize"
        # 'redirect_uri': "https://puresxciety.com/oauth/callback/",
        # Parámetros para la redirección
        params = {
            'redirect_uri': "http://local.example.com/oauth/callback/",
            'client_id': '809da80a-7064-41f8-81d1-e492cdd93fce',  # Reemplaza con tu client_id
            'response_type': 'code',
            'scope': 'openid',
        }

        # Construir la URL de redirección a OAuth
        oauth_redirect_url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])

        # Redirigir a la URL de redirección
        print(oauth_redirect_url)
        return redirect(oauth_redirect_url)
class OAuthCallbackView(View):
    def get(self, request, *args, **kwargs):
        authorization_code = request.GET.get('code')
        if authorization_code:
            # Procesa el código de autorización (aquí puedes enviarlo para intercambiar por tokens)
            # ...

            return HttpResponse("Authorization code captured successfully.")
        else:
            return HttpResponse("Failed to capture authorization code.")

