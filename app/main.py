from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "¡Salus MVP funcionando en la nube!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
