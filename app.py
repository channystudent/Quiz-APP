from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO
from dicttoxml import dicttoxml
from flask_cors import CORS
import pandas as pd
import json
import sqlite3

# =====================================================
# Flask App Configuration
# =====================================================
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================================================
# Database Models (SQLAlchemy)
# =====================================================

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


# =====================================================
# Initialize Database Tables
# =====================================================

def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    # Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer TEXT
        )
    ''')

    # Add default admin
    cursor.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)", ('admin', '1234'))

    conn.commit()
    conn.close()

with app.app_context():
    db.create_all()
    init_db()

# =====================================================
# Admin Routes
# =====================================================

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login route"""
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
            return redirect(url_for('admin_dashboard'))
        else:
            flash('ឈ្មោះ ឬ ពាក្យសម្ងាត់ មិនត្រឹមត្រូវ!')
    return render_template('admin_login.html')


@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    """Admin dashboard for creating questions"""
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    # Create new question
    if request.method == 'POST':
        category = request.form['category']
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        answer = request.form['answer']

        cursor.execute('''INSERT INTO questions (category, question, option1, option2, option3, option4, answer)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (category, question, option1, option2, option3, option4, answer))
        conn.commit()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', questions=questions)


@app.route('/delete-question/<int:id>')
def delete_question(id):
    """Delete question from admin dashboard"""
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))


@app.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# =====================================================
# User Routes
# =====================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('សូមបំពេញឈ្មោះ និង ពាក្យសម្ងាត់!')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('ឈ្មោះមិនមានទេ!')
        return redirect(url_for('index'))
        
    if user.password != password:
        flash('ពាក្យសម្ងាត់មិនត្រឹមត្រូវ!')
        return redirect(url_for('index'))
    
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
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
            flash('ឈ្មោះមានរួចហើយ!')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('អ៊ីមែលមានរួចហើយ!')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('ចុះឈ្មោះជោគជ័យ! សូមចូលប្រើប្រាស់។')
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


# =====================================================
# Export User and Quiz Data
# =====================================================
@app.route('/export/<format>')
def export_data(format):
    users_df = pd.read_sql(User.query.statement, db.session.bind)
    results_df = pd.read_sql(QuizResult.query.statement, db.session.bind)
    buffer = BytesIO()

    if format == 'json':
        data = {'users': users_df.to_dict('records'), 'results': results_df.to_dict('records')}
        return jsonify(data)

    elif format == 'csv':
        users_df.to_csv(buffer, index=False)
        buffer.write(b"\n\nQuiz Results:\n")
        results_df.to_csv(buffer, index=False)
        buffer.seek(0)
        return send_file(buffer, mimetype='text/csv', as_attachment=True, download_name='quiz_data.csv')

    elif format == 'xml':
        data = {'users': users_df.to_dict('records'), 'results': results_df.to_dict('records')}
        xml = dicttoxml(data, custom_root='data', attr_type=False)
        return xml, 200, {'Content-Type': 'application/xml'}

    return jsonify({'error': 'Invalid format'}), 400













# @app.route('/admin-dashboard', methods=['GET', 'POST'])
# def admin_dashboard():
#     if 'admin' not in session:
#         return redirect(url_for('admin_login'))

#     conn = sqlite3.connect('quiz.db')
#     cursor = conn.cursor()

#     if request.method == 'POST':
#         category = request.form['category']
#         question = request.form['question']
#         option1 = request.form['option1']
#         option2 = request.form['option2']
#         option3 = request.form['option3']
#         option4 = request.form['option4']
#         answer = request.form['answer']

#         cursor.execute('''INSERT INTO questions (category, question, option1, option2, option3, option4, answer)
#                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
#                        (category, question, option1, option2, option3, option4, answer))
#         conn.commit()

#     cursor.execute("SELECT * FROM questions")
#     questions = cursor.fetchall()
#     conn.close()

#     return render_template('admin_dashboard.html', questions=questions)










# =====================================================
# Run App
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)





















































# from flask import Flask, render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== DATABASE MODELS ==========
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    questions = db.relationship('Question', backref='category', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.String(500), nullable=False)  # comma-separated
    correct = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# ========== ROUTES ==========
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        data = request.get_json()
        new_cat = Category(name=data['name'])
        db.session.add(new_cat)
        db.session.commit()
        return jsonify({'message': 'Category added'})
    else:
        cats = Category.query.all()
        return jsonify([{'id': c.id, 'name': c.name} for c in cats])

@app.route('/api/questions/<int:cat_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def questions(cat_id):
    if request.method == 'POST':
        data = request.get_json()
        q = Question(
            question=data['question'],
            options=','.join(data['options']),
            correct=data['correct'],
            category_id=cat_id
        )
        db.session.add(q)
        db.session.commit()
        return jsonify({'message': 'Question added'})

    elif request.method == 'GET':
        qs = Question.query.filter_by(category_id=cat_id).all()
        return jsonify([
            {'id': q.id, 'question': q.question,
             'options': q.options.split(','), 'correct': q.correct}
            for q in qs
        ])

    elif request.method == 'PUT':
        data = request.get_json()
        q = Question.query.get(data['id'])
        q.question = data['question']
        q.correct = data['correct']
        q.options = ','.join(data['options'])
        db.session.commit()
        return jsonify({'message': 'Updated'})

    elif request.method == 'DELETE':
        q = Question.query.get(request.args.get('id'))
        db.session.delete(q)
        db.session.commit()
        return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
