from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faculty.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(20))
    status = db.Column(db.String(20), default='present')  # 'present', 'busy', 'absent'

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = user.role
        
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    
    flash('Invalid credentials')
    return redirect(url_for('home'))

@app.route('/student_dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('home'))
    teachers = Teacher.query.all()
    return render_template('student_dashboard.html', teachers=teachers)

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect(url_for('home'))
    teacher = Teacher.query.filter_by(user_id=session['user_id']).first()
    return render_template('teacher_dashboard.html', teacher=teacher)

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    users = User.query.all()
    teachers = Teacher.query.all()
    return render_template('admin_dashboard.html', users=users, teachers=teachers)

@app.route('/update_status', methods=['POST'])
def update_status():
    if session.get('role') != 'teacher':
        return redirect(url_for('home'))
    
    teacher = Teacher.query.filter_by(user_id=session['user_id']).first()
    teacher.status = request.form['status']
    if request.form.get('room_number'):
        teacher.room_number = request.form['room_number']
    db.session.commit()
    return redirect(url_for('teacher_dashboard'))

@app.route('/admin/create_user', methods=['POST'])
def create_user():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    role = request.form['role']
    
    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    
    if role == 'teacher':
        teacher = Teacher(user_id=user.id, name=request.form['name'])
        db.session.add(teacher)
        db.session.commit()
    
    flash('User created successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    
    user = User.query.get(user_id)
    if user.role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        db.session.delete(teacher)
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)