from app import app
from flask import render_template, jsonify,request,redirect,url_for
from flask_login import login_required, current_user
from app.DAO.accPinjamanWaitDAO import AccStatusWaitDAO,rejectByIDDAO, acceptByIDDAO



@app.route("/Acc", methods=["GET"])
@login_required
def AccStatusWait():
    try:
        if request.method == 'GET':
            print("data acc wait sudah ada")
            return render_template("accPinjamanWait.html")
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 
        

@app.route("/Acc/Wait", methods=["GET","POST"])
@login_required
def getPinjamanStatusWait():
    try:
        if request.method == 'GET':
            data = AccStatusWaitDAO()
            print("data acc wait sudah ada",data)
            return jsonify({"data":data}),200
        if request.method =="POST":
            
            return jsonify({"message": "successful"}), 200 
            # return jsonify({"message": "successful", "redirect_url": url_for('buktilbyid', user_id = user_id, user_idnya=user_idnya, id_peminjam=id_peminjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 
    
@app.route("/Acc/Wait/reject", methods=["POST"])
def rejectByID():
    try:
        if request.method =="POST":
            idpeminjam = request.form['userId']
            print("idpeminjam")
            rejectByIDDAO(idpeminjam)
            return jsonify("ok"), 200 
            # return jsonify({"message": "successful", "redirect_url": url_for('buktilbyid', user_id = user_id, user_idnya=user_idnya, id_peminjam=id_peminjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 
    

@app.route("/Acc/Wait/accept", methods=["POST"])
def acceptByID():
    try:
        if request.method =="POST":
            idpeminjam = request.form['userId']
            print("idpeminjam")
            acceptByIDDAO(idpeminjam)
            return jsonify("ok"), 200 
            # return jsonify({"message": "successful", "redirect_url": url_for('buktilbyid', user_id = user_id, user_idnya=user_idnya, id_peminjam=id_peminjam)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 
        
           
if __name__ == '__main__':
    app.run(debug=True)