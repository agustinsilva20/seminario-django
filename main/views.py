from django.shortcuts import render, redirect
from .decorators import login_obligatorio
from .querys import *
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
    cuenta = sql_obtener_cuenta_by_hash(request.COOKIES.get('pure_valorant_token'))
    dto = {
            "curso_owner": [],
            "curso_alumno": [],
            "nombre_usuario": "",
            "curso_owner_error": "",
            "curso_alumno_error": "",
        }
    try:
        id_persona = cuenta[0][0]
        dto["nombre_usuario"] = cuenta[0][1]

        # Obtengo los cursos
        curso_owner = sql_get_cursos_owner(id_persona)
        curso_alumno = sql_get_cursos_alumno(id_persona)

        if len(curso_owner) == 0:
            dto["curso_owner_error"] = "No tienes cursos creados"
        else:
            dto["curso_owner"] = curso_owner
        
        if len(curso_alumno) == 0:
            dto["curso_alumno_error"] = "No perteneces a ningun curso"
        else:
            dto["curso_alumno"] = curso_alumno
        print(curso_alumno)

        return render(request, 'home.html',dto)
    except Exception as e:
        # Cambiar a error
        print(e)
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

@login_obligatorio
def crearcurso(request):
    dto = {
        "error": "",
        "valor_user":""
    }
    cuenta = sql_obtener_cuenta_by_hash(request.COOKIES.get('pure_valorant_token'))

    if request.method == 'GET':
        return render(request, "crearcurso.html", dto)
    elif request.method == "POST":
        idcuenta = cuenta[0][0]
        nombrecurso = request.POST.get('nombrecurso')
        nombrecolegio = request.POST.get('nombrecolegio')
        curso = request.POST.get('curso')

        codigo_valido = False
        while not codigo_valido:
            # Creo un codigo
            caracteres = string.ascii_letters + string.digits
            codigo = ''.join(random.choice(caracteres) for _ in range(5))
            codigo = codigo.upper()
            # Valido que el codigo no exista
            query = sql_verificar_codigo(codigo)
            if len(query) == 0:
                codigo_valido = True
        sql_crear_curso(nombrecurso, idcuenta,nombrecolegio,curso, codigo)
        return redirect('home')

@login_obligatorio  
def joincurso(request):
    if request.method == "POST":
        cuenta = sql_obtener_cuenta_by_hash(request.COOKIES.get('pure_valorant_token'))
        idcuenta = cuenta[0][0]
        idcurso = request.POST.get('id_curso') 
        sql_join_curso(idcurso, idcuenta)
    return redirect('home')

@login_obligatorio
def detalle_curso(request, curso_id):
    cuenta = sql_obtener_cuenta_by_hash(request.COOKIES.get('pure_valorant_token'))
    idcuenta = cuenta[0][0]

    # Analizo si el usuario es Owner del curso
    owner_query = sql_get_cursos_owner(curso_id)
    owner = False
    if len(owner_query)>0:
        owner = True

    # Analizo si el usuario pertenece al curso
    query = sql_get_alumno_in_curso(curso_id, idcuenta)
    if len(query) == 0:
        if not owner:
            return HttpResponse(f'El usuario no pertenece a ese curso')
        
    # Obtengo la informacion del curso
    curso_info = sql_get_curso_info(curso_id)
    alumnos = sql_get_alumnos(curso_id)
    nombre = sql_get_nombre(idcuenta)

    print(curso_info)
    # Preparo el DTO
    dto = {
        "owner": owner,
        "id": curso_info[0][0],
        "materia": curso_info[0][1],
        "colegio": curso_info[0][3],
        "curso": curso_info[0][4],
        "codigo": curso_info[0][5],
        "cantidad_alumnos": len(alumnos),
        "docente": nombre[0][1],
        "encuesta_realizada": False
    }

    if owner:
        return render(request, "curso_docente.html", dto)
    else:
        return render(request, "curso_docente.html", dto)
    
@login_obligatorio
def crear_encuesta(request,curso_id):
    cuenta = sql_obtener_cuenta_by_hash(request.COOKIES.get('pure_valorant_token'))
    idcuenta = cuenta[0][0]
    # Analizo si el usuario es Owner del curso
    owner_query = sql_get_cursos_owner(curso_id)
    owner = True # Change
    if len(owner_query)>0:
        owner = True

    if not owner:
        return HttpResponse(f'El usuario no es administrador del curso')
    
    if request.method == "GET":
        
        
        dto = {
            "idcurso": curso_id
        }
        return render(request, "crear_encuesta.html", dto)
    
    elif request.method == "POST":
        pregunta1 = request.POST.get('pregunta1')
        pregunta2 = request.POST.get('pregunta2')
        pregunta3 = request.POST.get('pregunta3')
        pregunta4 = request.POST.get('pregunta4')
        pregunta5 = request.POST.get('pregunta5')
        pregunta6 = request.POST.get('pregunta6')
        pregunta7 = request.POST.get('pregunta7')

        sql_crear_encuesta(curso_id, pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6, pregunta7)

        return redirect('home')
    





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


