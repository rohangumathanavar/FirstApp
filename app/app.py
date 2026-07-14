from flask import Flask
import mysql.connector
import os

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50)
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()


@app.route("/")
def home():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()

        cursor.close()
        conn.close()

        return f"MySQL Version: {version[0]}"

    except Exception as e:
        return str(e)


@app.route("/add/<name>")
def add_user(name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name) VALUES (%s)",
            (name,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return f"{name} added successfully"

    except Exception as e:
        return str(e)


@app.route("/users")
def users():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        result = ""

        for row in rows:
            result += f"{row[0]} - {row[1]}<br>"

        return result

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000)
