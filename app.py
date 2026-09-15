from flask import Flask,render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url=request.form["long_url"]
    return long_url

if __name__ == "__main__":
    app.run(debug=True)