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

        # Verifica si la tabla existe, si no, la crea
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CUENTAS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME TEXT NOT NULL,
                PASSWORD TEXT NOT NULL,
                MAIL TEXT NOT NULL,
                TOKEN_CONEXION TEXT,
                RIOT TEXT
            )
        ''')

        # Inserta la nueva cuenta
        cursor.execute('''
            INSERT INTO CUENTAS (USERNAME, PASSWORD, MAIL, TOKEN_CONEXION, RIOT)
            VALUES (?, ?, ?, ?, ?)
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

    # Verifica si la tabla existe, si no, la crea
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CUENTAS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            MAIL TEXT NOT NULL,
            TOKEN_CONEXION TEXT,
            RIOT TEXT
        )
    ''')

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

    # Verifica si la tabla existe, si no, la crea
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CUENTAS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            MAIL TEXT NOT NULL,
            TOKEN_CONEXION TEXT NOT NULL,
            RIOT TEXT NOT NULL
        )
    ''')

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

    # Verifica si la tabla existe, si no, la crea
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CUENTAS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            MAIL TEXT NOT NULL,
            TOKEN_CONEXION TEXT NOT NULL,
            RIOT TEXT NOT NULL
        )
    ''')

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
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
