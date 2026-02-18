import mysql.connector

DB_HOST = "dbs.spskladno.cz"
DB_USER = "student14"
DB_PASS = "spsnet"
DB_NAME = "vyuka14"
DB_PORT = 3306

def get_conn(): # funkce která vytvoří a vrátí nové připojení do databáze
    return mysql.connector.connect( # zavolá connect z mysql.connector a vytvoří spojení
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
    )

def get_or_create_player_id(username: str) -> int:  # funkce: vezme username a vrátí player_id; když hráč neexistuje, vytvoří ho
    username = (username or "").strip() # ošetření vstupu: když je None -> "", a strip odstraní mezery na začátku/konci
    if not username: # pokud po ořezání nic nezbylo
        raise ValueError("Empty username") # vyhodí chybu, aby se do DB neukládal prázdný hráč

    conn = get_conn()  # vytvoří nové připojení do DB
    try:  # try/finally: zajistí že se spojení vždy zavře i když nastane chyba
        cur = conn.cursor() # cursor je objekt, přes který posíláš SQL dotazy a čteš výsledky

        #hledani existujícího hráče se stejným jménem
        cur.execute("SELECT player_id FROM players WHERE username=%s ORDER BY player_id DESC LIMIT 1", (username,)) # execute pošle SQL dotaz do databáze
        row = cur.fetchone() # parametry dotazu: %s se nahradí hodnotou username (bezpečně, ne ručně stringem)
        if row:  # pokud dotaz něco našel
            return int(row[0]) # row[0] je player_id, vrátí se jako int a funkce končí

        #jinak založ nového
        cur.execute("INSERT INTO players (username) VALUES (%s)", (username,))  # pokud hráč neexistuje, provede se INSERT
        conn.commit()  # commit potvrdí změny (INSERT) v databázi
        return int(cur.lastrowid)   # lastrowid = id právě vloženého hráče; vrátí se jako player_id

    finally: # finally proběhne vždy (i když nahoře return nebo chyba)
        conn.close() # zavře DB připojení

def save_game(username: str, mode_id: int, score: int) -> None:  # uloží jeden výsledek hry do tabulky games
    player_id = get_or_create_player_id(username)  # získá player_id: buď existuje, nebo se vytvoří nový hráč

    conn = get_conn() # nové připojení do DB (zvlášť pro insert do games)
    try:
        cur = conn.cursor() # cursor na provádění SQL
        cur.execute(  # INSERT do games = uloží výsledek konkrétní hry
            "INSERT INTO games (player_id, mode_id, score, player_at) VALUES (%s, %s, %s, NOW())", # NOW() = aktuální čas na DB serveru
            (player_id, int(mode_id), int(score)), # parametry dotazu: uloží player_id + mode_id + score; int()
        )
        conn.commit()  # commit potvrdí insert (uloží řádek do games)
    finally:
        conn.close()  # vždy zavře DB připojení