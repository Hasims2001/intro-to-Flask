from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key =True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(300), nullable=False)
    
#     def __init__(self, username, email, passowrd):
#         self.username = username
#         self.email = email
#         self.passowrd = passowrd



@app.route('/register', methods=["GET","POST"])
def register():
    user = request.get_json()
    if("password" in user):
        hashed = pbkdf2_sha256.using(rounds=10, salt_size=16).hash(user['password'])
        user['password'] = hashed
        session['username']= user['name']
        return jsonify({'message': 'User registered successfully','status':"success" ,'user': user})
    else:
        return jsonify({"message": "password not found", 'status': 'failed'})

    

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        user = request.get_json()
        if("password" in user):
            # pbkdf2_sha256.verify(user['passsword'],  stored_passwod)
            return jsonify({'message': 'User Login successfully','status':"success" ,'user': user})
        else:
            return jsonify({"message": "password not found or password is wrong", 'status': 'failed'})

    return '''
	<html>
    <body>
   <form action = "" method = "post">
      <p><input type = text name = username/></p>
      <p><input type = email name = email/></p>
      <p><input type = password name = password/></p>
      <p<button type = submit value = Login></button></p>
   </form>
   </body>
	</html>
   '''
@app.route('/profile', methods=["POST"])
def profile():
    pass


if __name__ == '__main__':
    app.run()