from flask import Flask, request, render_template, redirect, url_for, session
from database import db_session, init_db
from model.User import User
from model.Content import Content
from model.Favorite import Favorite
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/user-change-password', methods=['GET', 'POST'])
def user_change_password():
    if request.method == 'GET':
        return render_template('user-change-password.html', type=session['type'], email=session['email'])
    else:
        if request.form['password'] != request.form['confirm_password']:
            return render_template('user-change-password.html', error='Passwords do not match')
        user = User.query.filter_by(email=session['email']).first()
        if user.password == hashlib.md5(request.form['old_password'].encode('utf-8')).hexdigest():
            user.password = hashlib.md5(request.form['new_password'].encode('utf-8')).hexdigest()
            db_session.commit()
            return redirect(url_for('user-mine'), type=session['type'], email=session['email'])
        else:
            return render_template('user-change-password.html', error='Incorrect password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == None or password == None or email == '' or password == '':
            return render_template('login.html', error='Please enter your email and password')
        user = db_session.query(User).filter_by(email=email).first()
        if user == None:
            return render_template('login.html', error='User not found')
        hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        if user.password == hash_password:
            session['email'] = email
            return redirect(url_for('index'))
    return render_template('login.html', type=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['password1']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        age = request.form['age']
        if email == None or password == None or password1 == None or first_name == None or last_name == None or gender == None or age == None or \
            email == '' or password == '' or password1 == '' or first_name == '' or last_name == '' or gender == '' or age == '':
            return render_template('register.html', error='All field must be input')
        if password != password1:
            return render_template('register.html', error='Confirm password not equal to password')
        user = db_session.query(User).filter_by(email=email).first()
        if user != None:
            return render_template('register.html', error='User already exists')
        hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        user = User(email, hash_password)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', type=None)

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('type', None)
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        email=session.get('email'),
        type=session.get('type')
    )

@app.route('/user-manager', methods=['GET', 'POST'])
def user_manager():
    if request.method == 'POST':
        email = request.form['deleteEmail']
        user = db_session.query(User).filter_by(email=email).first()
        db_session.delete(user)
        db_session.commit()
    if not session['email']:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('user-manager.html', email=session['email'], users=users)

@app.route('/content-manager', methods=['GET', 'POST'])
def content_manager():
    if request.method == 'POST':
        id = request.form.get('deleteContentId')
        favorite_id = request.form.get('favoriteContentId')
        if id:
            content = db_session.query(Content).filter_by(id=id).first()
            db_session.delete(content)
            db_session.commit()

            favorites = db_session.query(Favorite).filter_by(content_id=id).all()
            for favorite in favorites:
                db_session.delete(favorite)
                db_session.commit()
        if favorite_id:
            favorite = Favorite(email=session['email'], content_id=favorite_id)
            db_session.add(favorite)
            db_session.commit()
    if not session or not session['email']:
        return redirect(url_for('login'))
    contents = Content.query.all()
    return render_template('content-manager.html', email=session['email'], contents=contents)

@app.route('/favorite-manager', methods=['GET', 'POST'])
def favorite_manager():
    if request.method == 'POST':
        id = request.form['favoriteContentId']
        content = db_session.query(Favorite).filter_by(id=id).first()
        db_session.delete(content)
        db_session.commit()
    if not session or not session['email']:
        return redirect(url_for('login'))
    contents = db_session.query(Favorite).filter_by(email=session['email']).all()
    return render_template('favorite-manager.html', email=session['email'], contents=contents)

# =============================================
# ==================== API ====================
# =============================================
@app.route('/api/login', methods=['POST'])
def api_login():
    # json request
    email = request.json['email']
    password = request.json['password']
    user = db_session.query(User).filter_by(email=email).first()
    if user == None:
        return 'User not found'
    hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if user.password == hash_password:
        return 'Login success'
    return 'Login failed'

@app.route('/api/register', methods=['POST'])
def api_register():
    email = request.json['email']
    password = request.json['password']
    password1 = request.json['password1']
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    if email == None or password == None or password1 == None or first_name == None or last_name == None or \
        email == '' or password == '' or password1 == '' or first_name == '' or last_name == '':
        return 'All field must be input'
    if password != password1:
        return 'Confirm password not equal to password'
    user = db_session.query(User).filter_by(email=email).first()
    if user != None:
        return 'User already exists'
    hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    user = User(email, hash_password)
    db_session.add(user)
    db_session.commit()
    return 'Register success'

@app.route('/api/contents', methods=['GET'])
def api_contents():
    contents = Content.query.all()
    result = []
    for content in contents:
        result.append({
            'title': content.title,
            'content': content.content,
            'from_url': content.from_url
        })
    return {'contents': result, 'status': 'success'}

@app.route('/api/favorites', methods=['POST'])
def api_favorites():
    email = request.json['email']
    favorites = db_session.query(Favorite).filter_by(email=email).all()
    result = []
    for favorite in favorites:
        result.append({
            'id': favorite.id,
            'email': email,
            'content_id': favorite.content_id
        })
    return {'favorites': result, 'status': 'success'}

@app.route('/api/favorite', methods=['POST'])
def api_favorite():
    email = request.json['email']
    content_id = request.json['content_id']
    favorite = Favorite(email, content_id)
    db_session.add(favorite)
    db_session.commit()
    return { 'status': 'success' }

@app.cli.command('init_db')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.cli.command('spider')
def spider_command():
    """Run the spider."""
    from spider import spider
    spider()
    print('Spider done.')
