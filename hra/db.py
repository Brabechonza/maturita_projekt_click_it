import mysql.connector

DB_HOST = "dbs.spskladno.cz"
DB_USER = "student14"
DB_PASS = "spsnet"
DB_NAME = "vyuka14"
DB_PORT = 3306

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
    )

def get_or_create_player_id(username: str) -> int:
    username = (username or "").strip()
    if not username:
        raise ValueError("Empty username")

    conn = get_conn()
    try:
        cur = conn.cursor()

        # 1) zkus najít existujícího hráče se stejným jménem
        cur.execute("SELECT player_id FROM players WHERE username=%s ORDER BY player_id DESC LIMIT 1", (username,))
        row = cur.fetchone()
        if row:
            return int(row[0])

        # 2) jinak založ nového
        cur.execute("INSERT INTO players (username) VALUES (%s)", (username,))
        conn.commit()
        return int(cur.lastrowid)

    finally:
        conn.close()

def save_game(username: str, mode_id: int, score: int) -> None:
    player_id = get_or_create_player_id(username)

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO games (player_id, mode_id, score, player_at) VALUES (%s, %s, %s, NOW())",
            (player_id, int(mode_id), int(score)),
        )
        conn.commit()
    finally:
        conn.close()