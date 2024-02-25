import os
from app import app
from flask import jsonify,request,render_template,url_for
from app.DAO.buktiPinjamanDAO import getUsersBuktiPeminjamDAO
from flask_login import login_required, current_user
from datetime import datetime


@app.route("/bukti", methods=["POST"])
@login_required
def Bukti():
    try:

        if request.method =="POST":
            print("berhasil masukana id bukti")
            id_peminjam = request.form['userId']
            print(id_peminjam)
            
            user_id= current_user.username
            user_idnya= current_user.id
        
            # return jsonify({"message": "successful"}), 200 
            return jsonify({"message": "successful", "redirect_url": url_for('buktilbyid', user_id = user_id, user_idnya=user_idnya, id_peminjam=id_peminjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 


@app.route("/bukti/<user_id>/<user_idnya>/<id_peminjam>", methods=["GET"])
@login_required
def buktilbyid(user_id, user_idnya, id_peminjam):
    try:
        # Lakukan operasi lain yang diperlukan dengan data yang diterima
        # Sebagai contoh, Anda bisa menggunakan data ini untuk mengambil informasi dari database

        # Contoh: Membuat data yang akan diteruskan ke template
        data = {
            'user_id': user_id,
            'user_idnya': user_idnya,
            'id_peminjam': id_peminjam
        }
        print("apakah adas data bukti")
        print(data)

        return render_template('buktiPeminjam.html', data=data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve bukti"}), 500




@app.route('/api/data/pinjaman/bukti', methods=["POST"])
def getUsersBuktiPeminjam():
    try:
        
        id_peminjam = request.form['id_peminjam'] 
        data = getUsersBuktiPeminjamDAO(id_peminjam)
        print("data bukti",data)
        return jsonify({"data":data}),200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500




if __name__ == '__main__':
    app.run(debug=True)