from app.settings.query import get_db_connection
from app import app
from flask_login import current_user

def getUsersBuktiPeminjamDAO(id_peminjam):
    conn = get_db_connection()
    cur = conn.cursor()
    query ='''select d3.id, d2.nama as id2,d1.nama as id1, d3.jumlah_pinjam, d3.tanggal, d3.bukti_bayar
            from "pinjam_db".pinjaman  d3
            INNER JOIN "pinjam_db".use d1 ON d3.idpeminjam = d1.id
            INNER JOIN "pinjam_db".use d2 ON d3.iddipimjam = d2.id
            where  d3.id =%(id_peminjam)s;
            '''
    params = {'id_peminjam':id_peminjam}
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


