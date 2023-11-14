import sqlite3
def borrarTabla():
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS CUENTAS')
    conn.commit()
    conn.close()
    print("DONE")

def select_all():
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CUENTAS')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def sql_crear_cuenta(username, password, mail):
    try:
        # Conecta a la base de datos
        conn = sqlite3.connect('pure_valorant.db')
        cursor = conn.cursor()

        # Inserta la nueva cuenta
        cursor.execute('''
            INSERT INTO CUENTAS (USERNAME, PASSWORD, MAIL, TOKEN_CONEXION)
            VALUES (?, ?, ?, ?)
        ''', (username, password, mail, None, None))

        # Confirma la transacción y cierra la conexión
        conn.commit()
        conn.close()
        print("Cuenta importada exitosamente.")
    except Exception as e:
        print(f"Error al importar la cuenta: {str(e)}")


def sql_obtener_cuenta_by_nombre(username):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Ejecuta la consulta
    query = f"SELECT * FROM CUENTAS WHERE USERNAME='{username}';"
    cursor.execute(query)

    # Obtiene los resultados
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()
    return resultados # Devuelve una lista

def sql_obtener_cuenta_by_mail(mail):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Ejecuta la consulta
    query = f"SELECT * FROM CUENTAS WHERE MAIL='{mail}';"
    cursor.execute(query)

    # Obtiene los resultados
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()
    return resultados # Devuelve una lista

def sql_obtener_cuenta_by_hash(hash):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Ejecuta la consulta
    query = f"SELECT * FROM CUENTAS WHERE TOKEN_CONEXION='{hash}';"
    cursor.execute(query)

    # Obtiene los resultados
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()
    return resultados # Devuelve una lista

def sql_insert_hash(hash, username):
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = f'UPDATE CUENTAS set TOKEN_CONEXION = "{hash}" WHERE USERNAME = "{username}"'
    cursor.execute(query)
    conn.commit()
    conn.close()

def sql_crear_curso(nombre, id_creador):
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    # Inserta el nuevo curso
    query = f" INSERT INTO CURSOS (NOMBRE_CURSO, ID_CURSO) VALUES ({nombre}, {id_creador})"

    cursor.execute(query)
    conn.commit()
    conn.close()


def sql_unirse_curso(id_curso, id_persona):
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    # Inserta el nuevo curso
    query = f" INSERT INTO INSCRIPCIONES (ID_CURSO, ID_CUENTA) VALUES ({id_curso}, {id_persona})"

    cursor.execute(query)
    conn.commit()
    conn.close()

def sql_get_cursos_owner(id_persona):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Ejecuta la consulta
    query = f"SELECT * FROM CURSOS WHERE ID_CUENTA='{id_persona}';"
    cursor.execute(query)

    # Obtiene los resultados
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()
    return resultados # Devuelve una lista

def sql_get_cursos_alumno(id_persona):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Ejecuta la consulta
    query = f"SELECT * FROM INSCRIPCIONES LEFT JOIN CURSOS ON INSCRIPCIONES.ID_CURSO = CURSOS.ID WHERE INSCRIPCIONES.ID_CUENTA='{id_persona}';"
    cursor.execute(query)

    # Obtiene los resultados
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()
    return resultados # Devuelve una lista
