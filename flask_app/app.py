import os
from flask import Flask, render_template
import pymysql
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "ews"),
        cursorclass=pymysql.cursors.DictCursor
    )

app = Flask(__name__)

@app.route("/")
def index():
    # Simple DB connectivity smoke test (optional)
    db_status = "SKIPPED"
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        conn.close()
        db_status = "OK"
    except Exception as e:
        db_status = f"ERROR: {e}"

    return render_template("index.html", db_status=db_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
