from flask import Flask, jsonify
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/jokes", methods=["GET"])
def get_jokes():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dadjokes;")
            rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

@app.route("/jokes/<int:joke_id>", methods=["GET"])
def get_joke(joke_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dadjokes WHERE id = %s;", (joke_id,))
            row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"error": "Joke not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
