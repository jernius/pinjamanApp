import os
from app import app
from flask import jsonify,request,render_template,url_for
from app.DAO.detailPinjamanDAO import getUsersDetailPinjamanDAO, createPaymentNoAllDAO, updateStatusToPendingNoAll
from flask_login import login_required, current_user
from datetime import datetime


@app.route("/detail", methods=["POST"])
@login_required
def detail():
    try:

        if request.method =="POST":
            print("berhasil masukana detail")
            iduserdipinjam = request.form['iduserdipinjam']
            print(iduserdipinjam)
            user_id= current_user.username
            user_idnya= current_user.id
            print(user_idnya)
            print(user_id)
            # return jsonify({"message": "successful"}), 200 
            return jsonify({"message": "successful", "redirect_url": url_for('detailbyid', user_id = user_id, user_idnya=user_idnya, iddipinjam=iduserdipinjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 


@app.route("/detail/<user_id>/<user_idnya>/<iddipinjam>", methods=["GET"])
@login_required
def detailbyid(user_id, user_idnya, iddipinjam):
    try:
        # Lakukan operasi lain yang diperlukan dengan data yang diterima
        # Sebagai contoh, Anda bisa menggunakan data ini untuk mengambil informasi dari database

        # Contoh: Membuat data yang akan diteruskan ke template
        data = {
            'user_id': user_id,
            'user_idnya': user_idnya,
            'iddipinjam': iddipinjam
        }

        return render_template('detailPinjaman.html', data=data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve details"}), 500




@app.route('/api/data/pinjaman/detail', methods=["POST"])
def getUsersDetailPinjaman():
    try:
        
        iddipinjam = request.form['iddipinjam'] 
        data = getUsersDetailPinjamanDAO(iddipinjam)
        return jsonify({"data":data}),200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500





UPLOAD_FOLDER = 'images'
STATIC_FOLDER = 'app/static'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)
if not os.path.exists(os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)):
    os.makedirs(os.path.join(STATIC_FOLDER, UPLOAD_FOLDER))


@app.route("/api/payment/detail", methods=["POST"])
def createPaymentNoAll():
    try:
        id_dibayar = request.form['id_dibayar']
        print(id_dibayar)
        file = request.files['file']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"proof_payment_{timestamp}.jpg"  # Ganti .jpg dengan ekstensi file yang sesuai 
        print(file)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        createPaymentNoAllDAO(filename,id_dibayar)

        # Panggil createPaymentDAO dan tangkap nilai yang dikembalikan
        iddipimjam, idpeminjam = createPaymentNoAllDAO(filename, id_dibayar)
        print("iddipimjam:", iddipimjam)
        print("idpeminjam:", idpeminjam)


        if iddipimjam is not None and idpeminjam is not None:
        #     # Lakukan sesuatu dengan iddipimjam dan idpeminjam, misalnya update status
            updateStatusToPendingNoAll(iddipimjam, idpeminjam)
    
        return jsonify({"message": "Payment created successfully", "filename": filename}), 200
        # return jsonify({"message": "ok"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to create user"}), 500



if __name__ == '__main__':
    app.run(debug=True)