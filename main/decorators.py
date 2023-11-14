# accounts/decorators.py

from django.shortcuts import redirect
from django.urls import reverse
from .querys import sql_obtener_cuenta_by_hash

def login_obligatorio(view_func):
    def wrapper(request, *args, **kwargs):
        # Verificar si el token está presente en las cookies
        try:
            token = request.COOKIES.get('pure_valorant_token')
        except:
            print("No se encontro cookie")
            token = None

        if token is not None:
            # Si hay un token verifico que sea valido
            query = sql_obtener_cuenta_by_hash(token)
            if len(query) != 0:
                return view_func(request, *args, **kwargs)
            else: 
                # El usuario no está autenticado, redirigir al login
                print("No se encontro cookie1")
                return redirect(reverse('login'))  # Reemplaza 'login' con tu URL de inicio de sesión

        else:
            # El usuario no está autenticado, redirigir al login
            print("No se encontro cookie2")
            return redirect(reverse('login'))  # Reemplaza 'login' con tu URL de inicio de sesión

    return wrapper
