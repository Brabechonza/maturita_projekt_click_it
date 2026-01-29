import mysql.connector

def save_score(name, score):
    conn = mysql.connector.connect(
        host="dbs.spskladno.cz",
        user="student14",
        password="spsnet",
        database="vyuka14",
        port=3306
    )

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scores (name, score) VALUES (%s, %s)",
        (name, score)
    )

    conn.commit()
    cur.close()
    conn.close()