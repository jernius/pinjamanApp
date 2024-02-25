from app.settings.query import get_db_connection
from app import app

def createUserDAO(name,enail,pas,code):
    conn = get_db_connection()
    print("masuk ke dao")
    cur = conn.cursor()
    query ='''
            INSERT INTO "pinjam_db".use (nama, email , pass, code_trans) VALUES 
            (%(name)s,%(enail)s, %(pas)s, %(code)s);
            '''
    params = {'name':name,'enail':enail, 'pas':pas, 'code':code }
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data





def getUserByEmail(email):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''
            SELECT * FROM "pinjam_db".use
            WHERE email = %(email)s;
            '''
    params = {'email':email }
    try:
        cur.execute(query, params)
        data = cur.fetchall()
        # print(data)
    except Exception as e:
        print(f"Error executing query: {e}")
    cur.close()
    conn.close()
    return data

def getCodeByCode(code):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''
            SELECT * FROM "pinjam_db".use
            WHERE code_trans = %(code)s;
            '''
    params = {'code':code }
    try:
        cur.execute(query, params)
        data = cur.fetchone()
        # print(data)
    except Exception as e:
        print(f"Error executing query: {e}")
    cur.close()
    conn.close()
    return data



def getUserByid(id):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''
            SELECT * FROM "pinjam_db".use
            WHERE id = %(id)s;
            '''
    params = {'id':id }
    try:
        cur.execute(query, params)
        data = cur.fetchall()
        # print(data)
    except Exception as e:
        print(f"Error executing query: {e}")
    cur.close()
    conn.close()
    return data