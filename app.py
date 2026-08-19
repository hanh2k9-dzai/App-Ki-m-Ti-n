from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "smart_reward_secret_key"

# Bộ danh sách câu hỏi về Việt Nam
QUESTIONS_DB = [
    {
        "id": 1,
        "question": "Thủ đô của Việt Nam là gì?",
        "options": ["A. TP. Hồ Chí Minh", "B. Hà Nội", "C. Đà Nẵng", "D. Cần Thơ"],
        "answer": "B. Hà Nội",
        "points": 100
    },
    {
        "id": 2,
        "question": "Thành phố nào được mệnh danh là 'Thành phố ngàn hoa'?",
        "options": ["A. Nha Trang", "B. Đà Lạt", "C. Sa Pa", "D. Huế"],
        "answer": "B. Đà Lạt",
        "points": 100
    },
    {
        "id": 3,
        "question": "Ngọn núi nào cao nhất Việt Nam và được gọi là 'Nóc nhà Đông Dương'?",
        "options": ["A. Fansipan", "B. Mẫu Sơn", "C. Ba Vì", "D. Langbiang"],
        "answer": "A. Fansipan",
        "points": 100
    },
    {
        "id": 4,
        "question": "Con sông nào dài nhất chảy qua lãnh thổ Việt Nam?",
        "options": ["A. Sông Hồng", "B. Sông Đồng Nai", "C. Sông Mê Kông", "D. Sông Đà"],
        "answer": "C. Sông Mê Kông", "points": 100
    },
    {
        "id": 5,
        "question": "Đảo lớn nhất của Việt Nam tên là gì?",
        "options": ["A. Cát Bà", "B. Phú Quốc", "C. Côn Đảo", "D. Lý Sơn"],
        "answer": "B. Phú Quốc",
        "points": 100
    },
    {
        "id": 6,
        "question": "Vịnh Hạ Long thuộc tỉnh nào của Việt Nam?",
        "options": ["A. Hải Phòng", "B. Quảng Ninh", "C. Nam Định", "D. Thanh Hóa"],
        "answer": "B. Quảng Ninh",
        "points": 100
    },
    {
        "id": 7,
        "question": "Món ăn nào của Việt Nam được coi là quốc phục ẩm thực và nổi tiếng toàn thế giới?",
        "options": ["A. Bún đậu mắm tôm", "B. Phở", "C. Bánh xèo", "D. Cơm tấm"],
        "answer": "B. Phở",
        "points": 100
    }
]

@app.route('/')
def home():
    # Giả lập điểm người dùng nếu chưa có session
    if 'user_points' not in session:
        session['user_points'] = 12580
    return render_template('index.html', user={'points': session['user_points']})

@app.route('/quiz')
def quiz():
    # Lấy ngẫu nhiên 1 câu hỏi từ danh sách
    q = random.choice(QUESTIONS_DB)
    return render_template('quiz.html', question=q)

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    q_id = data.get('question_id')
    selected_opt = data.get('answer')

    # Tìm câu hỏi tương ứng
    q = next((item for item in QUESTIONS_DB if item["id"] == q_id), None)
    
    if q and selected_opt == q['answer']:
        session['user_points'] = session.get('user_points', 0) + q['points']
        return jsonify({
            'status': 'success',
            'message': f'Chính xác! Bạn nhận được +{q["points"]} POINT',
            'new_points': session['user_points']
        })
    else:
        return jsonify({
            'status': 'wrong',
            'message': f'Rất tiếc, đáp án đúng là: {q["answer"] if q else ""}',
            'new_points': session.get('user_points', 0)
        })

if __name__ == '__main__':
    app.run(debug=True)
