import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Adiarinkadaddy@22041426',
    'database': 'security'
}

def create_connection():
    return mysql.connector.connect(**db_config)

def add_user(username, password):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO log (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        return False

def validate_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM log WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None
