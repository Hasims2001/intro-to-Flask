from flask import Flask, jsonify, request, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename  
import os  
from passlib.hash import pbkdf2_sha256
app = Flask(__name__)
app.secret_key = 'secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['MAX_CONTENT_LENGTH']= 5 * 1024 * 1024
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    filename = db.Column(db.String(255), nullable=True)
    path = db.Column(db.String(255), nullable=True)

    def __init__(self, username, email, password, filename, path): 
        self.username = username
        self.email = email
        self.password = password  
        self.filename = filename
        self.path = path

with app.app_context():
    db.create_all()

@app.route('/register', methods=["GET","POST"])
def register():
    # user = request.get_json()
    if('username' in session):
        return "already registerd user"
    
    if(request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed = pbkdf2_sha256.using(rounds=10, salt_size=16).hash(password)
        new_user = User(username=username, email=email, password=hashed, filename=None, path=None)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('profile'))
        # return jsonify({'message': 'User registered successfully', 'status': "success", 'user': user})
    return render_template('register.html')


@app.route('/login', methods=["GET","POST"]) 
def login():
    if('username' in session):
        return "already logged in user"
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        
        # user = request.get_json()
       
    
   
        stored_user = User.query.filter_by(email=email).first()
        stored_password = stored_user.password
        session['username'] = stored_user.username

        if pbkdf2_sha256.verify(password, stored_password):
            return redirect(url_for('profile', user=stored_user))
            # return jsonify({'message': 'User Login successfully', 'status': "success", 'user': user})
        else:
            return render_template('login.html', error='Password is wrong!')
            # return jsonify({"message": "password is wrong", 'status': 'failed'})

    return render_template('login.html')



@app.route("/profile", methods=['GET','POST'])
def profile():
    if('username' not in session):
        return render_template('login.html')
    
    if(request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # pic = request.files['pic']
        # print(pic)
        if(username == '' or email == '' or password == ''):
            return 'all fields are required!'
        
        hashed = pbkdf2_sha256.using(rounds=10, salt_size=16).hash(password)
        stored_user = User.query.filter_by(email=email).first()
        # if(pic):
        #     pic_filename = secure_filename(pic.filename)
        #     pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_filename))
        #     stored_user.filename = pic_filename
        #     stored_user.path = os.path.join(app.config['UPLOAD_FOLDER'], pic_filename)
       
        if(stored_user):
            stored_user.username = username
            stored_user.password = hashed
        
        db.session.commit()
        return 'Updated Succefully'
    stored_user = User.query.filter_by(username=session['username']).first()
    return render_template('profile.html', user=stored_user)
    


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
