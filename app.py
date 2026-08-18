from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>App Kiếm Tiền</h1>
    <p>Web đang hoạt động!</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
