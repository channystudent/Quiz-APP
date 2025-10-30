from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import pandas as pd
import sqlite3
from io import BytesIO
from dicttoxml import dicttoxml

app = Flask(__name__)
app.secret_key = 'replace-this-with-a-secure-random-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.Column(db.Text)  # Store JSON string of answers

with app.app_context():
    db.create_all()







@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin'] = username
            return redirect('/admin-dashboard')
        else:
            return "Invalid credentials"
    
    # For GET request, show the login form
    return render_template('admin_login.html')


@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin-login')

    if request.method == 'POST':
        category = request.form['category']
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        answer = request.form['answer']

        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO question (category, question, option1, option2, option3, option4, answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (category, question, option1, option2, option3, option4, answer))
        conn.commit()
        conn.close()

        return "Question added successfully!"
    
    return render_template('admin_dashboard.html')







@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('Please enter both username and password')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('Username not found')
        return redirect(url_for('index'))
        
    if user.password != password:
        flash('Incorrect password')
        return redirect(url_for('index'))
    
    # Login successful
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    # require login
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('quiz.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password=password  # In a real app, hash this password!
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    result = QuizResult(
        user_id=data['user_id'],
        score=data['score'],
        answers=json.dumps(data['answers'])
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({'message': 'Quiz submitted successfully'})

@app.route('/export/<format>')
def export_data(format):
    # Create DataFrames from the database tables
    users_df = pd.read_sql(User.query.statement, db.session.bind)
    results_df = pd.read_sql(QuizResult.query.statement, db.session.bind)
    
    # Create a BytesIO object to store the output
    buffer = BytesIO()
    
    if format == 'json':
        data = {
            'users': users_df.to_dict('records'),
            'results': results_df.to_dict('records')
        }
        return jsonify(data)
    
    elif format == 'csv':
        # Export both tables to CSV with a separator
        users_df.to_csv(buffer, index=False)
        buffer.write(b"\n\nQuiz Results:\n")
        results_df.to_csv(buffer, index=False)
        
        # Prepare the response
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name='quiz_data.csv'
        )
    
    elif format == 'xml':
        # Convert DataFrames to dictionaries
        data = {
            'users': users_df.to_dict('records'),
            'results': results_df.to_dict('records')
        }
        xml = dicttoxml(data, custom_root='data', attr_type=False)
        return xml, 200, {'Content-Type': 'application/xml'}
    
    else:
        return jsonify({'error': 'Invalid format'}), 400

if __name__ == '__main__':
    app.run(debug=True)