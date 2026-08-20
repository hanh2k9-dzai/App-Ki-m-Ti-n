from flask import Flask, render_template, jsonify, session, request
from datetime import date, timedelta
import random


app = Flask(__name__)

# ==================================================
# SESSION DEMO
# ==================================================

app.secret_key = "do-vui-doi-qua-demo-secret-key"


# ==================================================
# BẢNG ĐIỂM DANH
# ==================================================

CHECKIN_REWARDS = {
    1: 100,
    2: 120,
    3: 144,
    4: 173,
    5: 207,
    6: 249,
    7: 299
}


# ==================================================
# BẢNG QUY ĐỔI XU
#
# xu -> tiền VNĐ
# ==================================================

WITHDRAW_OPTIONS = {
    6000: 5000,
    11000: 10000,
    21000: 20000,
    51000: 50000,
    101000: 100000,
    201000: 200000,
    501000: 500000
}


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
# HÀM KHỞI TẠO SESSION
# ==================================================

def init_user_session():

    if "score" not in session:
        session["score"] = 0

    if "checkin_streak" not in session:
        session["checkin_streak"] = 0

    if "last_checkin" not in session:
        session["last_checkin"] = None

    if "checkin_history" not in session:
        session["checkin_history"] = []

    if "withdraw_history" not in session:
        session["withdraw_history"] = []


# ==================================================
# TRANG CHỦ
# ==================================================

@app.route("/")
def home():

    init_user_session()

    return render_template("index.html")


# ==================================================
# TRANG QUIZ
# ==================================================

@app.route("/quiz")
def quiz():

    init_user_session()

    session["used_questions"] = []

    session["question_count"] = 0

    session["answered_questions"] = []

    return render_template("quiz.html")


# ==================================================
# API LẤY ĐIỂM
# ==================================================

@app.route("/api/score")
def get_score():

    init_user_session()

    return jsonify({
        "score": session.get("score", 0)
    })


# ==================================================
# HÀM TÍNH NGÀY ĐIỂM DANH
# ==================================================

def get_checkin_state():

    today = date.today()

    last_checkin_string = session.get(
        "last_checkin"
    )

    streak = int(
        session.get(
            "checkin_streak",
            0
        )
    )

    checked_today = (
        last_checkin_string ==
        today.isoformat()
    )


    # Nếu đã nghỉ quá 1 ngày
    if last_checkin_string:

        try:

            last_date = date.fromisoformat(
                last_checkin_string
            )

            days_gap = (
                today - last_date
            ).days

            if days_gap > 1:

                streak = 0

        except ValueError:

            streak = 0


    if checked_today:

        current_day = max(
            1,
            min(streak, 7)
        )

    else:

        current_day = streak + 1

        if current_day > 7:
            current_day = 1


    reward = CHECKIN_REWARDS[
        current_day
    ]


    return {
        "today": today,
        "streak": streak,
        "checked_today": checked_today,
        "next_day": current_day,
        "next_reward": reward
    }


# ==================================================
# API ĐIỂM DANH
#
# GET  = xem trạng thái
# POST = nhận điểm
# ==================================================

@app.route(
    "/api/checkin",
    methods=["GET", "POST"]
)
def checkin():

    init_user_session()

    state = get_checkin_state()


    # ==================================================
    # GET
    # ==================================================

    if request.method == "GET":

        history = session.get(
            "checkin_history",
            []
        )

        done_days = set()

        today = state["today"]

        # Chỉ lấy lịch sử 7 ngày gần nhất
        for item in history:

            try:

                item_date = date.fromisoformat(
                    item["date"]
                )

                diff = (
                    today - item_date
                ).days

                if 0 <= diff <= 6:

                    done_days.add(
                        item["day"]
                    )

            except Exception:

                pass


        days = []

        for day in range(1, 8):

            days.append({

                "day": day,

                "reward":
                    CHECKIN_REWARDS[day],

                "done":
                    day in done_days,

                "current":
                    day == state["next_day"]

            })


        return jsonify({

            "success": True,

            "streak":
                state["streak"],

            "checked_today":
                state["checked_today"],

            "next_day":
                state["next_day"],

            "next_reward":
                state["next_reward"],

            "days":
                days

        })


    # ==================================================
    # POST
    # ==================================================

    if state["checked_today"]:

        return jsonify({

            "success": False,

            "message":
                "Hôm nay bạn đã điểm danh rồi!",

            "streak":
                state["streak"],

            "checked_today":
                True,

            "next_day":
                state["next_day"],

            "next_reward":
                state["next_reward"]

        }), 400


    # Nếu hôm trước có điểm danh
    if state["streak"] > 0:

        last_checkin_string = session.get(
            "last_checkin"
        )

        try:

            last_date = date.fromisoformat(
                last_checkin_string
            )

            if (
                state["today"] -
                last_date
            ).days == 1:

                new_streak = (
                    state["streak"] + 1
                )

                if new_streak > 7:
                    new_streak = 1

            else:

                new_streak = 1

        except Exception:

            new_streak = 1

    else:

        new_streak = 1


    # Ngày thứ 8 quay lại ngày 1
    if new_streak > 7:
        new_streak = 1


    reward = CHECKIN_REWARDS[
        new_streak
    ]


    # Cộng xu
    session["score"] = (
        session.get("score", 0)
        + reward
    )


    # Lưu streak
    session["checkin_streak"] = (
        new_streak
    )


    # Lưu ngày
    session["last_checkin"] = (
        state["today"].isoformat()
    )


    # Lưu lịch sử
    history = session.get(
        "checkin_history",
        []
    )

    history.append({

        "date":
            state["today"].isoformat(),

        "day":
            new_streak,

        "reward":
            reward

    })


    # Giữ tối đa 30 lần
    session["checkin_history"] = (
        history[-30:]
    )


    session.modified = True


    return jsonify({

        "success": True,

        "message":
            f"Điểm danh ngày {new_streak} thành công! +{reward:,} xu",

        "reward":
            reward,

        "streak":
            new_streak,

        "checked_today":
            True,

        "next_day":
            new_streak,

        "next_reward":
            reward,

        "score":
            session.get("score", 0)

    })


# ==================================================
# API LẤY CÂU HỎI
# ==================================================

@app.route("/api/question")
def get_question():

    used_questions = session.get(
        "used_questions",
        []
    )


    if len(used_questions) >= len(
        QUESTIONS
    ):

        used_questions = []


    available_questions = [

        i
        for i in range(
            len(QUESTIONS)
        )
        if i not in used_questions

    ]


    question_id = random.choice(
        available_questions
    )


    used_questions.append(
        question_id
    )


    session["used_questions"] = (
        used_questions
    )


    session["question_count"] = (
        session.get(
            "question_count",
            0
        ) + 1
    )


    question = QUESTIONS[
        question_id
    ]


    return jsonify({

        "id":
            question_id,

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

            "message":
                "Không có dữ liệu"

        }), 400


    question_id = data.get(
        "question_id"
    )

    answer = data.get(
        "answer"
    )


    if question_id is None or answer is None:

        return jsonify({

            "success": False,

            "message":
                "Dữ liệu không hợp lệ"

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

            "message":
                "Dữ liệu không hợp lệ"

        }), 400


    if (
        question_id < 0
        or
        question_id >= len(QUESTIONS)
    ):

        return jsonify({

            "success": False,

            "message":
                "Không tìm thấy câu hỏi"

        }), 404


    question = QUESTIONS[
        question_id
    ]


    correct_answer = question[
        "correct"
    ]


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

            "points":
                0,

            "score":
                session.get(
                    "score",
                    0
                ),

            "already_answered":
                True

        })


    is_correct = (
        answer == correct_answer
    )


    points = 0


    if is_correct:

        points = 10

        session["score"] = (
            session.get(
                "score",
                0
            ) + points
        )


    answered_questions.append(
        question_id
    )


    session[
        "answered_questions"
    ] = answered_questions


    session.modified = True


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
# API AI
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
# TRANG RÚT TIỀN
# ==================================================

@app.route("/rut-tien")
def rut_tien():

    init_user_session()

    return render_template(
        "rut_tien.html",
        score=session.get(
            "score",
            0
        ),
        options=WITHDRAW_OPTIONS
    )


# ==================================================
# API RÚT TIỀN
# ==================================================

@app.route(
    "/api/withdraw",
    methods=["POST"]
)
def withdraw():

    init_user_session()


    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({

            "success": False,

            "message":
                "Dữ liệu không hợp lệ"

        }), 400


    try:

        coins = int(
            data.get("coins")
        )

    except:

        return jsonify({

            "success": False,

            "message":
                "Số xu không hợp lệ"

        }), 400


    # Kiểm tra gói rút
    if coins not in WITHDRAW_OPTIONS:

        return jsonify({

            "success": False,

            "message":
                "Mức rút không hợp lệ"

        }), 400


    current_score = int(
        session.get(
            "score",
            0
        )
    )


    if current_score < coins:

        return jsonify({

            "success": False,

            "message":
                f"Bạn cần {coins:,} xu nhưng hiện chỉ có {current_score:,} xu",

            "score":
                current_score

        }), 400


    money = WITHDRAW_OPTIONS[
        coins
    ]


    # Trừ xu
    session["score"] = (
        current_score - coins
    )


    # Lưu lịch sử rút
    history = session.get(
        "withdraw_history",
        []
    )


    history.append({

        "coins":
            coins,

        "money":
            money,

        "status":
            "demo",

        "date":
            date.today().isoformat()

    })


    session["withdraw_history"] = (
        history[-50:]
    )


    session.modified = True


    return jsonify({

        "success": True,

        "message":
            f"Rút demo thành công {money:,}đ",

        "coins":
            coins,

        "money":
            money,

        "remaining_score":
            session["score"],

        "status":
            "demo"

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

