from flask import Flask, render_template, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "do-vui-doi-qua-demo-secret-key"


# =========================
# NGÂN HÀNG CÂU HỎI
# =========================

QUESTIONS = [
    {
        "question": "Thủ đô của Việt Nam là gì?",
        "answers": [
            "Hà Nội",
            "Hải Phòng",
            "Đà Nẵng",
            "Huế"
        ],
        "correct": 0
    },

    {
        "question": "Một tuần có bao nhiêu ngày?",
        "answers": [
            "5 ngày",
            "6 ngày",
            "7 ngày",
            "8 ngày"
        ],
        "correct": 2
    },

    {
        "question": "Hành tinh nào gần Mặt Trời nhất?",
        "answers": [
            "Trái Đất",
            "Sao Hỏa",
            "Sao Kim",
            "Sao Thủy"
        ],
        "correct": 3
    },

    {
        "question": "2 + 8 × 2 bằng bao nhiêu?",
        "answers": [
            "20",
            "18",
            "16",
            "12"
        ],
        "correct": 1
    },

    {
        "question": "Loài vật nào được gọi là chúa sơn lâm?",
        "answers": [
            "Voi",
            "Hổ",
            "Gấu",
            "Sói"
        ],
        "correct": 1
    },

    {
        "question": "Nước đóng băng ở khoảng bao nhiêu độ C?",
        "answers": [
            "0°C",
            "10°C",
            "50°C",
            "100°C"
        ],
        "correct": 0
    },

    {
        "question": "Màu tạo ra khi trộn đỏ và vàng là gì?",
        "answers": [
            "Xanh lá",
            "Tím",
            "Cam",
            "Đen"
        ],
        "correct": 2
    },

    {
        "question": "Việt Nam nằm ở khu vực nào của châu Á?",
        "answers": [
            "Đông Nam Á",
            "Tây Á",
            "Nam Á",
            "Bắc Á"
        ],
        "correct": 0
    },

    {
        "question": "Thiết bị nào thường dùng để chụp ảnh?",
        "answers": [
            "Camera",
            "Loa",
            "Router",
            "Bàn phím"
        ],
        "correct": 0
    },

    {
        "question": "Một năm thông thường có bao nhiêu tháng?",
        "answers": [
            "10",
            "11",
            "12",
            "13"
        ],
        "correct": 2
    }
]


# =========================
# TRANG CHỦ
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# TRANG QUIZ
# =========================

@app.route("/quiz")
def quiz():
    # Reset phiên chơi
    session["score"] = 0
    session["question_count"] = 0
    session["used_questions"] = []

    return render_template("quiz.html")


# =========================
# LẤY CÂU HỎI NGẪU NHIÊN
# =========================

@app.route("/api/question")
def get_question():

    used = session.get("used_questions", [])

    # Nếu đã dùng hết câu hỏi thì tạo lại danh sách
    if len(used) >= len(QUESTIONS):
        used = []

    available = [
        i for i in range(len(QUESTIONS))
        if i not in used
    ]

    question_index = random.choice(available)

    used.append(question_index)

    session["used_questions"] = used
    session["question_count"] = session.get(
        "question_count", 0
    ) + 1

    question = QUESTIONS[question_index]

    return jsonify({
        "id": question_index,
        "question": question["question"],
        "answers": question["answers"],
        "number": session["question_count"],
        "total": len(QUESTIONS)
    })


# =========================
# KIỂM TRA ĐÁP ÁN
# =========================

@app.route("/api/answer", methods=["POST"])
def check_answer():

    from flask import request

    data = request.get_json()

    question_id = data.get("question_id")
    answer = data.get("answer")

    if question_id is None or answer is None:
        return jsonify({
            "success": False,
            "message": "Dữ liệu không hợp lệ"
        }), 400

    try:
        question_id = int(question_id)
        answer = int(answer)
    except:
        return jsonify({
            "success": False,
            "message": "Dữ liệu không hợp lệ"
        }), 400

    if question_id < 0 or question_id >= len(QUESTIONS):
        return jsonify({
            "success": False,
            "message": "Không tìm thấy câu hỏi"
        }), 404

    question = QUESTIONS[question_id]

    correct_answer = question["correct"]

    if answer == correct_answer:

        # +10 điểm demo
        session["score"] = session.get("score", 0) + 10

        return jsonify({
            "correct": True,
            "correct_answer": correct_answer,
            "points": 10,
            "score": session["score"],
            "message": "🎉 Chính xác! +10 điểm"
        })

    else:

        return jsonify({
            "correct": False,
            "correct_answer": correct_answer,
            "points": 0,
            "score": session.get("score", 0),
            "message": "❌ Chưa chính xác!"
        })


# =========================
# API LẤY ĐIỂM HIỆN TẠI
# =========================

@app.route("/api/score")
def get_score():

    return jsonify({
        "score": session.get("score", 0)
    })


# =========================
# CÁC ROUTE DEMO
# =========================

@app.route("/vip")
def vip():
    return "Trang Đặc quyền VIP"


@app.route("/ai-quiz")
def ai_quiz():
    return "Trang Hỏi AI - Demo"


@app.route("/rut-tien")
def rut_tien():
    return "Trang Rút điểm - Demo"


@app.route("/moi-ban")
def moi_ban():
    return "Trang Mời bạn bè - Demo"


@app.route("/tui-mu")
def tui_mu():
    return "Trang Túi mù - Demo"


@app.route("/huong-dan")
def huong_dan():
    return "Trang Hướng dẫn - Demo"


@app.route("/thong-tin")
def thong_tin():
    return "Trang Thông tin web - Demo"


@app.route("/nhiem-vu")
def nhiem_vu():
    return "Trang Nhiệm vụ - Demo"


@app.route("/cskh")
def cskh():
    return "Trang CSKH - Demo"


# =========================
# CHẠY SERVER
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
