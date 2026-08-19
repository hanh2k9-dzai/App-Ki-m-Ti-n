from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    return render_template("index.html", page="quiz")


@app.route("/vip")
def vip():
    return render_template("index.html", page="vip")


@app.route("/ai-quiz")
def ai_quiz():
    return render_template("index.html", page="ai-quiz")


@app.route("/rut-tien")
def rut_tien():
    return render_template("index.html", page="rut-tien")


@app.route("/moi-ban")
def moi_ban():
    return render_template("index.html", page="moi-ban")


@app.route("/tui-mu")
def tui_mu():
    return render_template("index.html", page="tui-mu")


@app.route("/huong-dan")
def huong_dan():
    return render_template("index.html", page="huong-dan")


@app.route("/thong-tin")
def thong_tin():
    return render_template("index.html", page="thong-tin")


@app.route("/nhiem-vu")
def nhiem_vu():
    return render_template("index.html", page="nhiem-vu")


@app.route("/cskh")
def cskh():
    return render_template("index.html", page="cskh")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
