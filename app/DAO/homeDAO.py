from app.settings.query import get_db_connection
from flask_login import current_user



def getUsersPeminjamDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='SELECT * FROM "pinjam_db".use;'
    cur.execute(query)
    data = cur.fetchall()
    # print(data)
    cur.close()
    conn.close()
    return data


def getUserDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d3.id, d2.nama as id2,d1.nama as id1, d3.jumlah_pinjam, d3.tanggal, d3.bukti_bayar
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            where  d3.iddipimjam = %s and d3.status < 3;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print('ini datanya',data)
    cur.close()
    conn.close()
    return data

def getTotalPinjamanSatatusWaitDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''SELECT COUNT(*) AS jumlah
                FROM "pinjam_db".pinjaman
                WHERE idpeminjam = %s AND status = 4 ;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchone()
    print(data)
    cur.close()
    conn.close()
    return data

def getDataStatusWaitDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d3.id as id_pinjaman, d2.nama as iddipimjam ,d1.nama as idpeminjam , d3.jumlah_pinjam, d3.tanggal, d3.acc_danamasuk
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            where idpeminjam  = %s AND status = 4 ;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data

def getTotalPinjamanAccStatusWaitDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''SELECT COUNT(*) AS jumlah
                FROM "pinjam_db".pinjaman
                WHERE iddipimjam  = %s AND status = 4 and bukti_trasfer is null and acc_danamasuk = 0;;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchone()
    print(data)
    cur.close()
    conn.close()
    return data


def getUserdipinjamallDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d1.nama AS namaidpeminjam, d2.nama as namaiddipimjam,d2.id as ididdipimjam,sum(d3.jumlah_pinjam) AS total_pinjam,  d4.data_status as dataStatus
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            INNER JOIN "pinjam_db".status d4 ON d3.status  = d4.id
            where  d3.idpeminjam = %s and  d3.status = 1
            GROUP BY d2.id,d1.id, d4.id;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data

def AccDAO(id_pinjaman):
    conn = get_db_connection()
    cur = conn.cursor()
    query =''' 
            UPDATE "pinjam_db".pinjaman
            SET status = 3
            WHERE id = %(id_pinjaman)s ;
            '''
    params = {'id_pinjaman':id_pinjaman}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data


def getUserdipinjamallPendingDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d1.nama AS namaidpeminjam, d2.nama as namaiddipimjam,d2.id as ididdipimjam,sum(d3.jumlah_pinjam) AS total_pinjam,  d4.data_status as dataStatus
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            INNER JOIN "pinjam_db".status d4 ON d3.status  = d4.id
            where  d3.idpeminjam = %s and  d3.status = 2
            GROUP BY d2.id,d1.id, d4.id;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data

def getUserdipinjamallPaidDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d1.nama AS namaidpeminjam, d2.nama as namaiddipimjam,d2.id as ididdipimjam,sum(d3.jumlah_pinjam) AS total_pinjam,  d4.data_status as dataStatus
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            INNER JOIN "pinjam_db".status d4 ON d3.status  = d4.id
            where  d3.idpeminjam = %s and  d3.status = 3
            GROUP BY d2.id,d1.id, d4.id;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data

def getUserdipinjamDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d3.id, d2.nama as id2,d1.nama as id1, d3.jumlah_pinjam, d3.tanggal 
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            where  d3.idpeminjam = %s;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data


def selectIdWhereCode(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query ='''
                SELECT id FROM "pinjam_db".use WHERE code_trans = %(code)s;
                '''
        params = {'code':code}
        cur.execute(query, params)
        result = cur.fetchone()
        print("INI DATA UDAH KELUAR?",result)
        return result
    except Exception as e:
        print(f"Error in createPaymentDAO: {str(e)}")
        return None, None
    finally:
        cur.close()
        conn.close()


def createPinjamDAO(peminjam,id,nominal,tanggalpengembalian):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''
            INSERT INTO "pinjam_db".pinjaman (idpeminjam, iddipimjam, jumlah_pinjam, tanggalpengembalian ) VALUES 
            (%(peminjam)s,%(dipinjam)s, %(nominal)s, %(tanggalpengembalian)s);
            '''
    params = {'peminjam':peminjam, 'dipinjam':id,'nominal':nominal, 'tanggalpengembalian':tanggalpengembalian}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data

def deleteUsersDao(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query = 'DELETE FROM "pinjam_db".pinjaman WHERE id = %s;'
        print(query)
        cur.execute(query, (id,))
        result =  conn.commit()
        print("result", result)
    except Exception as e:
        conn.rollback()
        print ("e", e)
    cur.close()
    conn.close()
    return True


def createPaymentDAO(filename,id_dibayar):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query ='''
                UPDATE "pinjam_db".pinjaman
                SET bukti_bayar = %(filename)s
                WHERE iddipimjam = %(id_dibayar)s AND idpeminjam = %(id_pembayar)s
                RETURNING iddipimjam, idpeminjam;
                '''
        params = {'filename':filename, 'id_dibayar':id_dibayar,'id_pembayar':current_user.id}
        cur.execute(query, params)
        data = conn.commit()
        print(data)
        result = cur.fetchone()
        print(result)
        iddipimjam, idpeminjam = result if result else (None, None)
        return iddipimjam, idpeminjam
    except Exception as e:
        print(f"Error in createPaymentDAO: {str(e)}")
        return None, None
    finally:
        cur.close()
        conn.close()
    

def updateStatusToPending(iddipimjam, idpeminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''
            UPDATE "pinjam_db".pinjaman
            SET status = 2
            WHERE iddipimjam = %(iddipimjam)s AND idpeminjam = %(idpeminjam)s AND bukti_bayar IS NOT NULL;
            '''
    params = {'iddipimjam':iddipimjam, 'idpeminjam':idpeminjam}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data

def acc01ByIDDAO(idpeminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''UPDATE "pinjam_db".pinjaman
            SET status = 1
            WHERE id = %(id_pinjaman)s ;
            '''
    params = {'id_pinjaman':idpeminjam}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data


def reject01ByIDDAO(idpeminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''UPDATE "pinjam_db".pinjaman
            SET status = 5
            WHERE id = %(id_pinjaman)s ;
            '''
    params = {'id_pinjaman':idpeminjam}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data


    