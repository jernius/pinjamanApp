from app import app
from flask import render_template, jsonify,request,redirect,url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, current_user
from app.DAO.loginDAO import createUserDAO,getUserByEmail,getUserByid, getCodeByCode
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message



app.secret_key = 'afnacjlnldcfhnahdsjcbxcbadhfrfe'  # Change this to a secure secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'





class User(UserMixin):
    def __init__(self, id, username, email, password, code):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.code = code

@login_manager.user_loader
def load_user(id):
    userData = getUserByid(id)  
    if userData:
        print("data sudah sama?")
        # return User(userData[0][0], userData[0][1], userData[0][2],  userData[0][3]) 
        return User(*userData[0]) 
    else:
        return None
    


@app.route("/login", methods=["GET","POST"])
def getlogin():
    try:
        if request.method == 'GET':
            return render_template("login.html")
        if request.method =="POST":
            email = request.form["email"]
            pas = request.form["pass"]
            userData = getUserByEmail(email)
            print(userData)
            if userData is not None:
                 user = User(userData[0][0], userData[0][1], userData[0][2],  userData[0][3], userData[0][4])
                 print('userData')
                 if check_password_hash(user.password, pas) and user.email==email :
                     login_user(user)
                     print (current_user.id)
                     print("login berhasil")
                    #  return jsonify({"message": "Registration successful", "redirect_url": url_for('home')}), 200             
                     return jsonify({"login": url_for('home')})
                 else:
                        print("login gagal")
                        return jsonify({"message": "Failed login"}), 401 
            else:
                return jsonify({"message": "Failed login"}), 401
            
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to retrieve users"}), 500 



@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('getlogin'))

# ----------------------------


import random
import string

def generate_transaction_code(length=5):
    # Membuat kode transaksi acak dengan awalan 'J' dan diakhiri 'z', serta huruf besar
    letters_and_digits = string.ascii_uppercase + string.digits # berisi huruf besar dan digit
    transaction_code = 'J' + ''.join(random.choice(letters_and_digits) for _ in range(length - 2)) + 'Z' #membuat cede
    return transaction_code


def generate_unique_transaction_code():
    while True:
        code = generate_transaction_code()
        codez = getCodeByCode(code)
        # Memeriksa apakah kode sudah ada dalam database
        print(codez)
        if codez is None:
            # Kode belum ada, dapat digunakan
            return code  


def generate_random_code():
    # Menghasilkan kode validasi acak (contoh)
    return str(random.randint(1000, 9999))






# --------------------------------------
    
# Konfigurasi Flask-Mail
app.config['MAIL_SERVER'] = 'mail.jernsync.my.id'  # Ganti dengan alamat SMTP server Anda
app.config['MAIL_PORT'] = 465  # Ganti dengan port SMTP yang digunakan
app.config['MAIL_USE_TLS'] = False  # Gunakan TLS, sesuai dengan kebutuhan server Anda
app.config['MAIL_USE_SSL'] = True  # Jangan gunakan SSL jika menggunakan TLS
app.config['MAIL_USERNAME'] = 'admin@jernsync.my.id'  # Ganti dengan alamat email pengirim
app.config['MAIL_PASSWORD'] = 'jerzend09'  # Ganti dengan kata sandi email pengirim
app.config['MAIL_DEFAULT_SENDER'] = 'admin@jernsync.my.id'  # Ganti dengan alamat email pengirim default

mail = Mail(app)


@app.route('/validation', methods=["POST"])
def postvalidation():
    try:
            email = request.form.get('email')

            validation_code = generate_random_code()

            # Simpan validation_code di dalam sesi
            session['validation_code'] = validation_code

            send_validation_email(email, validation_code)

            return jsonify({"x": url_for('getlogin')})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500     



def send_validation_email(email, validation_code):

    print("cek")
    # Kirim email validasi
    msg = Message('Subject: Kode Validasi',
                  recipients=[email])
    msg.body = f'Kode validasi Anda: {validation_code}'
    mail.send(msg)


@app.route('/register', methods=["GET","POST"])
def getRegister():
    try:
        if request.method == 'GET':
            print("dfsdfds")
            return render_template('register.html')
        if request.method == 'POST':
            print("masuk post")
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["pass"]
            validasicode = request.form["validasicode"]
            validation_code = session.get('validation_code', None)
            print("validasi dari post register  ",validation_code)


            code = generate_unique_transaction_code()
            print("code ;",code)
            passhash = generate_password_hash(password)
            print("passhash ;",passhash)
            databyemail = getUserByEmail(email)

        
            print("databyemail ;",databyemail)            

            if validasicode != validation_code:
                print("masuk validasi tidak sama")
                error_response = {"error": "Silakan cek kembali code validasi."}
                print(error_response)
                return jsonify(error_response), 400


            if databyemail:
                error_response = {"error": "Email sudah digunakan. Silakan gunakan email lain."}
                print(error_response)
                return jsonify(error_response), 400
            
            # Membuat pengguna baru
            createUserDAO(name, email, passhash, code)
            print("Berhasil memasukkan data pengguna")
            return jsonify({"x": url_for('getlogin')}),200          
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to retrieve users"}), 500