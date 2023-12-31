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

def sql_crear_curso(nombrecurso, idcuenta,nombrecolegio,curso, codigo):
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    # Inserta el nuevo curso
    query = f' INSERT INTO CURSOS (NOMBRE_CURSO, ID_CUENTA, COLEGIO, CURSO, CODIGO) VALUES ("{nombrecurso}", "{idcuenta}","{nombrecolegio}", "{curso}", "{codigo}")'

    cursor.execute(query)
    conn.commit()
    conn.close()

def sql_verificar_codigo(codigo):
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    # Inserta el nuevo curso
    query = f' SELECT * FROM CURSOS WHERE CODIGO = "{codigo}"'
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultados



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

def sql_join_curso(codigo, idcuenta):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Verifico si existe el curso
    query = f"SELECT * FROM CURSOS WHERE CODIGO='{codigo}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    if len(resultados) == 0:
        print("El curso no existe")
        return
    
    # Verifico que el alumno no esta inscripto
    query = f"SELECT * FROM INSCRIPCIONES LEFT JOIN CURSOS ON INSCRIPCIONES.ID_CURSO = CURSOS.ID WHERE INSCRIPCIONES.ID_CUENTA='{idcuenta}' AND CURSOS.CODIGO='{codigo}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    if len(resultados)>0:
        print("El alumno ya se encuentra ingresado")
        return
    
    # Verifica que no sea owner
    query = f"SELECT * FROM CURSOS WHERE ID_CUENTA='{idcuenta}' AND CODIGO='{codigo}';"
    cursor.execute(query)
    resultados = cursor.fetchall()
    if len(resultados)>0:
        print("El usuario es owner")
        return

    
    # Inserto el nuevo registro
    print("Insertando alumno")

    query = f"SELECT ID FROM CURSOS WHERE CODIGO='{codigo}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    idcurso = resultados[0][0]
    query = f"INSERT INTO INSCRIPCIONES (ID_CURSO, ID_CUENTA) VALUES ({idcurso}, {idcuenta})"
    cursor.execute(query)
    conn.commit()
    conn.close()

def sql_get_alumno_in_curso(idcurso, idpersona):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Verifico si existe el curso
    query = f"SELECT * FROM INSCRIPCIONES WHERE ID_CURSO='{idcurso}' AND ID_CUENTA='{idpersona}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()

    return resultados

def sql_get_curso_info(idcurso):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = query = f"SELECT * FROM CURSOS WHERE CURSOS.ID='{idcurso}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()

    return resultados

def sql_get_alumnos(idcurso):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = query = f"SELECT USERNAME, MAIL FROM INSCRIPCIONES LEFT JOIN CUENTAS ON INSCRIPCIONES.ID_CUENTA = CUENTAS.ID WHERE ID_CURSO='{idcurso}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()

    return resultados

def sql_get_nombre(idpersona):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = query = f"SELECT * FROM CUENTAS WHERE ID='{idpersona}';"
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()

    return resultados

def sql_crear_encuesta(curso_id, pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6, pregunta7):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = f"INSERT INTO ENCUESTAS (ID_CURSO, PREGUNTA1, PREGUNTA2, PREGUNTA3, PREGUNTA4, PREGUNTA5, PREGUNTA6, PREGUNTA7) VALUES ('{curso_id}', '{pregunta1}','{pregunta2}','{pregunta3}','{pregunta4}','{pregunta5}','{pregunta6}','{pregunta7}')"
    cursor.execute(query)
    conn.commit()
    conn.close()



def sql_get_encuesta(curso_id):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = f"SELECT PREGUNTA1, PREGUNTA2, PREGUNTA3, PREGUNTA4, PREGUNTA5, PREGUNTA6, PREGUNTA7 FROM ENCUESTAS WHERE ID_CURSO='{curso_id}';"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def sql_get_respuestas_encuesta(curso_id):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = f"SELECT RESPUESTA1, RESPUESTA2, RESPUESTA3, RESPUESTA4, RESPUESTA5, RESPUESTA6, RESPUESTA7 FROM RESPUESTAS_ENCUESTA WHERE ID_ENCUESTA='{curso_id}';"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def sql_get_encuesta_respondida(cursoid, personaid):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM RESPUESTAS_ENCUESTA WHERE ID_ENCUESTA='{cursoid}' AND ID_CUENTA='{personaid}';"

    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    print(resultados)
    return resultados

def sql_agregar_respuesta(dto):
    id_cuenta = dto["id_cuenta"]
    id_encuesta = dto["id_encuesta"]
    respuesta1 = dto["respuesta1"]
    respuesta2 = dto["respuesta2"]
    respuesta3 = dto["respuesta3"]
    respuesta4 = dto["respuesta4"]
    respuesta5 = dto["respuesta5"]
    respuesta6 = dto["respuesta6"]
    respuesta7 = dto["respuesta7"]

    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()
    query = f' INSERT INTO RESPUESTAS_ENCUESTA (ID_CUENTA, ID_ENCUESTA, RESPUESTA1, RESPUESTA2, RESPUESTA3,RESPUESTA4,RESPUESTA5,RESPUESTA6,RESPUESTA7) VALUES ("{id_cuenta}", "{id_encuesta}","{respuesta1}","{respuesta2}","{respuesta3}","{respuesta4}","{respuesta5}","{respuesta6}","{respuesta7}")'
    cursor.execute(query)
    conn.commit()
    conn.close()

def sql_soy_owner(idpersona, idcurso):
    # Conecta a la base de datos
    conn = sqlite3.connect('pure_valorant.db')
    cursor = conn.cursor()

    # Ejecuta la consulta
    query = f"SELECT * FROM CURSOS WHERE ID_CUENTA='{idpersona}' and ID='{idcurso}';"
    cursor.execute(query)

    # Obtiene los resultados
    resultados = cursor.fetchall()

    # Cierra la conexión
    conn.close()
    return resultados # Devuelve una lista

    
    


    

