import os
import random
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "smart-reward-secret-key-change-this"

# Cấu hình SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Người Dùng
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    points = db.Column(db.Integer, default=12580)

# Model Câu Hỏi
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(10), nullable=False)
    reward = db.Column(db.Integer, default=100)

# Khởi tạo dữ liệu mẫu
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="SMART").first():
        db.session.add(User(username="SMART", points=12580))
        db.session.commit()
    
    if Question.query.count() == 0:
        sample_questions = [
            Question(title="Thủ đô của Việt Nam là gì?", option_a="TP.HCM", option_b="Hà Nội", option_c="Đà Nẵng", option_d="Cần Thơ", answer="B", reward=100),
            Question(title="Số nào sau đây là số nguyên tố?", option_a="4", option_b="6", option_c="7", option_d="9", answer="C", reward=150),
            Question(title="1 + 1 x 2 bằng bao nhiêu?", option_a="3", option_b="4", option_c="2", option_d="1", answer="A", reward=100)
        ]
        db.session.add_all(sample_questions)
        db.session.commit()

# Middleware giả lập user đăng nhập
@app.before_request
def set_default_user():
    session['username'] = "SMART"

# ROUTES GIAO DIỆN
@app.route('/')
def index():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('index.html', user=user)

@app.route('/quiz')
def quiz():
    questions = Question.query.all()
    q = random.choice(questions) if questions else None
    return render_template('quiz.html', question=q)

@app.route('/tasks')
def tasks():
    link_tasks = [
        {"id": 1, "title": "Nhiệm vụ Vượt Link #1 (YeoFast)", "reward": 500, "url": "#"},
        {"id": 2, "title": "Nhiệm vụ Vượt Link #2 (Droplink)", "reward": 800, "url": "#"},
        {"id": 3, "title": "Nhiệm vụ Xem Video 30s", "reward": 300, "url": "#"}
    ]
    return render_template('tasks.html', tasks=link_tasks)

@app.route('/wallet')
def wallet():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('wallet.html', user=user)

# API XỬ LÝ TRẢ LỜI CÂU HỎI
@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    q_id = data.get('question_id')
    user_choice = data.get('choice')

    question = Question.query.get(q_id)
    if not question:
        return jsonify({"status": "error", "message": "Câu hỏi không tồn tại!"})

    if user_choice == question.answer:
        user = User.query.filter_by(username=session['username']).first()
        user.points += question.reward
        db.session.commit()
        return jsonify({
            "status": "success", 
            "message": f"Chính xác! Bạn nhận được +{question.reward} Point.",
            "new_points": user.points
        })
    else:
        return jsonify({"status": "error", "message": "Đáp án chưa đúng, hãy thử lại!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
