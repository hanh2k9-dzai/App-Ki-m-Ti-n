from flask import Flask, render_template, jsonify, session, request
import random

app = Flask(__name__)

# Khóa session demo
app.secret_key = "do-vui-doi-qua-demo-secret-key"


# ==================================================
# NGÂN HÀNG CÂU HỎI
# ==================================================

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
    },

    {
        "question": "Đại dương lớn nhất trên Trái Đất là gì?",
        "answers": [
            "Đại Tây Dương",
            "Thái Bình Dương",
            "Ấn Độ Dương",
            "Bắc Băng Dương"
        ],
        "correct": 1
    },

    {
        "question": "Con vật nào thường được gọi là 'vua của muôn loài'?",
        "answers": [
            "Sư tử",
            "Hổ",
            "Voi",
            "Báo"
        ],
        "correct": 0
    }
]


# ==================================================
# CÂU HỎI AI DEMO
# ==================================================

AI_QUESTIONS = [
    {
        "question": "Số nào sau đây là số nguyên tố?",
        "answers": [
            "21",
            "27",
            "29",
            "33"
        ],
        "correct": 2
    },

    {
        "question": "Nếu hôm nay là thứ Hai, 10 ngày nữa là thứ mấy?",
        "answers": [
            "Thứ Tư",
            "Thứ Năm",
            "Thứ Sáu",
            "Thứ Bảy"
        ],
        "correct": 1
    },

    {
        "question": "Hành tinh nào gần Mặt Trời nhất?",
        "answers": [
            "Trái Đất",
            "Sao Hỏa",
            "Sao Thủy",
            "Sao Kim"
        ],
        "correct": 2
    },

    {
        "question": "Một giờ có bao nhiêu phút?",
        "answers": [
            "30",
            "45",
            "60",
            "90"
        ],
        "correct": 2
    }
]


# ==================================================
# TRANG CHỦ
# ==================================================

@app.route("/")
def home():

    # Nếu chưa có điểm thì tạo điểm = 0
    if "score" not in session:
        session["score"] = 0

    return render_template("index.html")


# ==================================================
# TRANG QUIZ
# ==================================================

@app.route("/quiz")
def quiz():

    # QUAN TRỌNG:
    # Không reset score khi vào lại Quiz.

    if "score" not in session:
        session["score"] = 0

    # Reset bộ câu hỏi của lượt chơi mới
    session["used_questions"] = []

    session["question_count"] = 0

    # Danh sách câu đã trả lời trong lượt hiện tại
    session["answered_questions"] = []

    return render_template("quiz.html")


# ==================================================
# API LẤY ĐIỂM
# ==================================================

@app.route("/api/score")
def get_score():

    return jsonify({
        "score": session.get("score", 0)
    })


# ==================================================
# API LẤY CÂU HỎI NGẪU NHIÊN
# ==================================================

@app.route("/api/question")
def get_question():

    used_questions = session.get(
        "used_questions",
        []
    )

    # Nếu đã dùng hết câu thì tạo lại
    if len(used_questions) >= len(QUESTIONS):

        used_questions = []

    # Tìm những câu chưa dùng
    available_questions = [
        i
        for i in range(len(QUESTIONS))
        if i not in used_questions
    ]

    # Chọn ngẫu nhiên
    question_id = random.choice(
        available_questions
    )

    # Lưu câu đã sử dụng
    used_questions.append(question_id)

    session["used_questions"] = used_questions

    session["question_count"] = (
        session.get("question_count", 0) + 1
    )

    question = QUESTIONS[question_id]

    return jsonify({

        "id": question_id,

        "question":
            question["question"],

        "answers":
            question["answers"],

        "number":
            session["question_count"],

        "total":
            len(QUESTIONS)

    })


# ==================================================
# API KIỂM TRA ĐÁP ÁN
# ==================================================

@app.route(
    "/api/answer",
    methods=["POST"]
)
def check_answer():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "success": False,
            "message": "Không có dữ liệu"
        }), 400


    question_id = data.get(
        "question_id"
    )

    answer = data.get(
        "answer"
    )


    # Kiểm tra dữ liệu
    if question_id is None or answer is None:

        return jsonify({
            "success": False,
            "message": "Dữ liệu không hợp lệ"
        }), 400


    try:

        question_id = int(
            question_id
        )

        answer = int(
            answer
        )

    except:

        return jsonify({
            "success": False,
            "message": "Dữ liệu không hợp lệ"
        }), 400


    # Kiểm tra ID câu hỏi
    if (
        question_id < 0
        or
        question_id >= len(QUESTIONS)
    ):

        return jsonify({
            "success": False,
            "message": "Không tìm thấy câu hỏi"
        }), 404


    question = QUESTIONS[
        question_id
    ]


    correct_answer = question[
        "correct"
    ]


    # ==================================================
    # CHỐNG TRẢ LỜI LẠI CÙNG MỘT CÂU
    # ==================================================

    answered_questions = session.get(
        "answered_questions",
        []
    )


    if question_id in answered_questions:

        return jsonify({

            "success": True,

            "correct":
                answer == correct_answer,

            "correct_answer":
                correct_answer,

            "points": 0,

            "score":
                session.get(
                    "score",
                    0
                ),

            "already_answered":
                True

        })


    # ==================================================
    # KIỂM TRA
    # ==================================================

    is_correct = (
        answer == correct_answer
    )


    points = 0


    if is_correct:

        # Đúng +10 điểm
        points = 10

        session["score"] = (
            session.get(
                "score",
                0
            ) + points
        )


    # Lưu câu đã trả lời
    answered_questions.append(
        question_id
    )

    session[
        "answered_questions"
    ] = answered_questions

    session.modified = True


    # ==================================================
    # TRẢ KẾT QUẢ
    # ==================================================

    if is_correct:

        message = (
            "🎉 Chính xác! +10 điểm"
        )

    else:

        message = (
            "❌ Chưa chính xác!"
        )


    return jsonify({

        "success": True,

        "correct":
            is_correct,

        "correct_answer":
            correct_answer,

        "points":
            points,

        "score":
            session.get(
                "score",
                0
            ),

        "message":
            message

    })


# ==================================================
# API AI TẠO CÂU HỎI DEMO
# ==================================================

@app.route("/api/ai-question")
def ai_question():

    question = random.choice(
        AI_QUESTIONS
    )

    return jsonify({

        "question":
            question["question"],

        "answers":
            question["answers"],

        "correct":
            question["correct"]

    })


# ==================================================
# CÁC TRANG DEMO
# ==================================================

@app.route("/vip")
def vip():

    return """
    <h2>👑 Đặc quyền VIP</h2>
    <a href="/">← Trang chủ</a>
    """


@app.route("/ai-quiz")
def ai_quiz():

    return """
    <h2>🤖 Hỏi AI</h2>
    <p>Tính năng AI đang được phát triển.</p>
    <a href="/quiz">← Quay lại Quiz</a>
    """


@app.route("/rut-tien")
def rut_tien():

    return """
    <h2>💳 Rút điểm</h2>
    <p>Tính năng đổi thưởng đang được phát triển.</p>
    <a href="/">← Trang chủ</a>
    """


@app.route("/moi-ban")
def moi_ban():

    return """
    <h2>🤝 Mời bạn bè</h2>
    <p>Tính năng mời bạn bè đang được phát triển.</p>
    <a href="/">← Trang chủ</a>
    """


@app.route("/tui-mu")
def tui_mu():

    return """
    <h2>🛍️ Túi mù</h2>
    <p>Tính năng túi mù đang được phát triển.</p>
    <a href="/">← Trang chủ</a>
    """


@app.route("/huong-dan")
def huong_dan():

    return """
    <h2>📖 Hướng dẫn</h2>
    <p>Hướng dẫn sử dụng website.</p>
    <a href="/">← Trang chủ</a>
    """


@app.route("/thong-tin")
def thong_tin():

    return """
    <h2>ℹ️ Thông tin web</h2>
    <p>Đố Vui Đổi Quà - bản demo.</p>
    <a href="/">← Trang chủ</a>
    """


@app.route("/nhiem-vu")
def nhiem_vu():

    return """
    <h2>🎯 Nhiệm vụ</h2>
    <p>Hệ thống nhiệm vụ đang được phát triển.</p>
    <a href="/">← Trang chủ</a>
    """


@app.route("/cskh")
def cskh():

    return """
    <h2>🎧 CSKH</h2>
    <p>Trang chăm sóc khách hàng.</p>
    <a href="/">← Trang chủ</a>
    """


# ==================================================
# CHẠY SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
