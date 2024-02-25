from app.settings.query import get_db_connection
from app import app
from flask_login import current_user

def getUsersDetailPinjamanDAO(iddipinjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d3.id, d2.nama as namadipinjam, d1.nama as namapeminjam, d3.jumlah_pinjam, d3.tanggal, d3.tanggalpengembalian 
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            where  d3.idpeminjam = %(peminjam)s and d3.iddipimjam = %(iddipinjam)s and d3.status = 1;
            '''
    print("cek kalau masuk query")
    params = {'peminjam':current_user.id, 'iddipinjam':iddipinjam}
    cur.execute(query, params)
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data

def createPaymentNoAllDAO(filename,id_dibayar):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query ='''
                UPDATE "pinjam_db".pinjaman
                SET bukti_bayar = %(filename)s
                WHERE id = %(id_dibayar)s AND idpeminjam = %(id_pembayar)s
                RETURNING id, idpeminjam;
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
    
def updateStatusToPendingNoAll(iddipimjam, idpeminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''
            UPDATE "pinjam_db".pinjaman
            SET status = 2
            WHERE id = %(iddipimjam)s AND idpeminjam = %(idpeminjam)s AND bukti_bayar IS NOT NULL;
            '''
    params = {'iddipimjam':iddipimjam, 'idpeminjam':idpeminjam}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data