from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import pandas as pd
from io import BytesIO
from dicttoxml import dicttoxml

app = Flask(__name__)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']  # In a real app, hash this password!
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registration successful'})
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