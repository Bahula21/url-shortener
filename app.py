from flask import Flask

app = Flask(__name__)

@app.route("/<short_code>")
def redirect(short_code):
    return short_code

if __name__ == "__main__":
    app.run(debug=True)