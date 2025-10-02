from tkinter.constants import BROWSE

from flask import jsonify
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

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

def get_joke_count():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as joke_count FROM dadjokes;")
            rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()



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

def add_joke(joke, punchline):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO dadjokes (joke, punchline) VALUES (%s, %s);", (joke,punchline))
            connection.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()