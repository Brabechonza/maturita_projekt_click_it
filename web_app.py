from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

DB_HOST = "dbs.spskladno.cz"
DB_USER = "student14"
DB_PASSWORD = "DOPLN_HESLO"
DB_NAME = "vyuka14"
DB_PORT = 3306

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

@app.get("/")
def home():
    return render_template("home.html")

@app.get("/leaderboard")
def leaderboard():
    con = get_conn()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT u.username, s.score, s.played_at
        FROM game_sessions s
        JOIN users u ON u.id = s.user_id
        ORDER BY s.score DESC, s.played_at DESC
        LIMIT 50;
    """)
    rows = cur.fetchall()

    cur.close()
    con.close()

    return render_template("leaderboard.html", rows=rows)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)