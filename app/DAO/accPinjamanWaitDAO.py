from app.settings.query import get_db_connection
from app import app
from flask_login import current_user

def AccStatusWaitDAO():
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d3.id as id_pinjaman, d2.nama as idpeminjam,d1.nama as iddipimjam, d3.jumlah_pinjam, d3.tanggal
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            where iddipimjam  = %s AND status = 4 and bukti_trasfer is null and acc_danamasuk = 0;
            '''
    print("cek kalau masuk query")
    cur.execute(query, (current_user.id,))
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data



def rejectByIDDAO(idpeminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''UPDATE "pinjam_db".pinjaman
            SET acc_danamasuk = 2
            WHERE id = %(id_pinjaman)s ;
            '''
    params = {'id_pinjaman':idpeminjam}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data

def acceptByIDDAO(idpeminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''UPDATE "pinjam_db".pinjaman
            SET acc_danamasuk = 1
            WHERE id = %(id_pinjaman)s ;
            '''
    params = {'id_pinjaman':idpeminjam}
    cur.execute(query, params)
    data = conn.commit()
    print(data)
    cur.close()
    conn.close()
    return data
