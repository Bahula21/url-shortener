from flask import Flask,render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)

def get_db():
    return sqlite3.connect("urls.db")

def init_db():
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT
        )
    """)

    connection.commit()
    connection.close()

def generate_short_code():
    short_code=""
    characters = string.ascii_letters + string.digits

    for i in range(6):
        short_code += random.choice(characters)

    return short_code

def code_exists(short_code):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT short_code FROM urls WHERE short_code = ? ", (short_code,)   
    )

    result = cursor.fetchone()

    connection.close()

    if result is not None:
        return True
    else:
        return False


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url=request.form["long_url"]

    if not long_url:
        return "Please enter a URL", 400

    if not long_url.startswith(("http://", "https://")):
        return "Invalid URL", 400

    short_code = generate_short_code()

    while(code_exists(short_code)):
        short_code = generate_short_code()

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO urls (short_code,long_url) VALUES (?,?)", (short_code, long_url)
    )

    connection.commit()
    connection.close()

    return "http://127.0.0.1:5000/" + short_code

@app.route("/<short_code>")
def redirect_to_url(short_code):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT long_url FROM urls WHERE short_code=?",(short_code,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return "Short URL not found",404

    return redirect(result[0])



init_db()

if __name__ == "__main__":
    app.run(debug=True)