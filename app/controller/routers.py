import os
from app import app
from flask import render_template, jsonify,request,redirect,url_for
from app.DAO.homeDAO import getUserDAO,createPinjamDAO,getUsersPeminjamDAO,getUserdipinjamallDAO, createPaymentDAO, updateStatusToPending,getUserdipinjamallPendingDAO,AccDAO, getUserdipinjamallPaidDAO, getTotalPinjamanSatatusWaitDAO, getTotalPinjamanAccStatusWaitDAO, getDataStatusWaitDAO, acc01ByIDDAO, reject01ByIDDAO, selectIdWhereCode
from flask_login import login_required, current_user, logout_user
from datetime import datetime




@app.route("/")
@login_required
def home():
    print("berhasil masukana home")
    user_id= current_user.username
    user_idnya= current_user.id
    user_code = current_user.code
    return render_template('home.html', user_id = user_id, user_idnya=user_idnya, user_code=user_code)





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('getlogin'))


# --------------------------------------------------



@app.route('/', methods=["POST"])
def createPinjam():
    try:
        nominal = request.form['nominal']
        code = request.form['code'] 
        peminjam = request.form['peminjam'] 
        tanggalpengembalian = request.form['tanggalpengembalian']

         # Panggil createPaymentDAO dan tangkap nilai yang dikembalikan
        id = selectIdWhereCode(code)
        print("ini id dari kode: ",id)
        if(id):
            createPinjamDAO(peminjam,id,nominal,tanggalpengembalian)
            print(nominal)
            return jsonify("ok"), 200
        else:
            return jsonify("Failed to create peminjam"), 500
    except Exception as e:
        print("Error:", str(e))
        return jsonify("Failed to create peminjam"), 500
    
@app.route('/acc', methods=["POST"])
def Acc():
    try:
        id_pinjaman = request.form['id_pinjaman']
        print("ini id peminjam", id_pinjaman)
        AccDAO(id_pinjaman)
        return jsonify("ok"), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify("Failed to create peminjam"), 500


@app.route('/peminjam', methods=["GET"])
def getUsersPeminjam():
    try:
        data = getUsersPeminjamDAO()
        return jsonify({"data":data}),200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500



@app.route('/api/data/pinjaman/all', methods=["GET"])
def getUserspinjamall():
    try:
        data = getUserdipinjamallDAO()
        return jsonify({"data":data}),200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500
    
@app.route('/api/data/pinjaman/all/pending', methods=["GET"])
def getUserspinjamallPending():
    try:
        data = getUserdipinjamallPendingDAO()
        return jsonify({"data":data}),200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500
    
    
@app.route('/api/data/pinjaman/all/paid', methods=["GET"])
def getUserspinjamallPaid():
    try:
        data = getUserdipinjamallPaidDAO()
        return jsonify({"data":data}),200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500




@app.route('/api/data', methods=["GET"])
def getUsers():
    try:
        data = getUserDAO()
        
        return jsonify({"data":data}),200
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500
    


# @app.route("/api/data", methods=["DELETE"])
# def delete_user():
#     try:
#         id= request.form['id']
#         # Panggil fungsi delete_user_dao untuk menghapus pengguna
#         deleteUsersDao(id)
#         print(id)
#         response = jsonify({"message": "User deleted successfully"}), 200
#         return response
#     except Exception as e:
#         print("Error:", str(e))
#         return jsonify({"error": "Failed to delete user"}), 500
    


UPLOAD_FOLDER = 'images'
STATIC_FOLDER = 'app/static/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)
if not os.path.exists(os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)):
    os.makedirs(os.path.join(STATIC_FOLDER, UPLOAD_FOLDER))

@app.route("/api/payment", methods=["POST"])
def createPayment():
    try:
        id_dibayar = request.form['id_dibayar']
        file = request.files['file']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"proof_payment_{timestamp}.jpg"  # Ganti .jpg dengan ekstensi file yang sesuai 
        print(file)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        createPaymentDAO(filename,id_dibayar)

        # Panggil createPaymentDAO dan tangkap nilai yang dikembalikan
        iddipimjam, idpeminjam = createPaymentDAO(filename, id_dibayar)
        print("iddipimjam:", iddipimjam)
        print("idpeminjam:", idpeminjam)


        if iddipimjam is not None and idpeminjam is not None:
        #     # Lakukan sesuatu dengan iddipimjam dan idpeminjam, misalnya update status
            updateStatusToPending(iddipimjam, idpeminjam)
    
        return jsonify({"message": "Payment created successfully", "filename": filename}), 200
        # return jsonify({"message": "ok"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to create user"}), 500

@app.route('/api/data/TotalWait', methods=["GET"])
def getTotalPinjamanSatatusWait():
    try:
        data = getTotalPinjamanSatatusWaitDAO()
        
        return jsonify({"data":data}),200
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500
    
@app.route('/api/data/Wait', methods=["GET"])
def getDataStatusWait():
    try:
        data = getDataStatusWaitDAO()
        
        return jsonify({"data":data}),200
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500
    

@app.route('/api/data/Acc/Wait', methods=["GET"])
def getTotalPinjamanAccStatusWait():
    try:
        data = getTotalPinjamanAccStatusWaitDAO()
        
        return jsonify({"data":data}),200
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500
    
@app.route("/api/data/Acc/Wait/accept", methods=["POST"])
def acc01ByID():
    try:
        if request.method =="POST":
            idpeminjam = request.form['userId']
            print("idpeminjam")
            acc01ByIDDAO(idpeminjam)
            return jsonify("ok"), 200 
            # return jsonify({"message": "successful", "redirect_url": url_for('buktilbyid', user_id = user_id, user_idnya=user_idnya, id_peminjam=id_peminjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 
    

@app.route("/api/data/Acc/Wait/reject", methods=["POST"])
def reject01ByID():
    try:
        if request.method =="POST":
            idpeminjam = request.form['userId']
            print("idpeminjam")
            reject01ByIDDAO(idpeminjam)
            return jsonify("ok"), 200 
            # return jsonify({"message": "successful", "redirect_url": url_for('buktilbyid', user_id = user_id, user_idnya=user_idnya, id_peminjam=id_peminjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 
    




if __name__ == '__main__':
    app.run(debug=True)