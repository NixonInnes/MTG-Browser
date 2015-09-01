import sqlite3
import requests

DB_FILENAME = "data/mtg.sqlite"

USER_SCHEMA = """
    CREATE TABLE users(
        username TEXT,
        password TEXT,
        mod_level INT,
        decks TEXT)
        """

CARDS_SCHEMA = """
    CREATE TABLE mtg_cards(
        layout TEXT,
        colors TEXT,
        power INT,
        name TEXT,
        subtypes TEXT,
        types TEXT,
        cmc INT,
        manaCost TEXT,
        imageName TEXT,
        text TEXT,
        type TEXT,
        toughness INT,
        supertypes TEXT,
        names TEXT,
        starter TEXT,
        hand TEXT,
        life INT,
        loyalty INT)
        """

def card_search(card):
    db = sqlite3.connect(DB_FILENAME)
    cur = db.cursor()
    search = "%"+card+"%"
    cur.execute('''
        SELECT name FROM mtg_cards WHERE name LIKE ?
        ''', (search,))
    data = cur.fetchall()

    if len(data) == 1:
        cur.execute('''
        SELECT * FROM mtg_cards WHERE name = ?
        ''', (data[0][0],))
        data = cur.fetchall()
    db.close()
    return data

def get_cards_json():
    try:
        cards = requests.get('http://mtgjson.com/json/AllCards.json').json()
        return cards
    except:
        return {}

def create_cards_table():
    # Connect to DB
    db = sqlite3.connect(DB_FILENAME)
    cur = db.cursor()

    # Drop the existing cards table
    cur.execute("DROP TABLE IF EXISTS mtg_cards")
    # Create a new fresh table
    cur.execute(CARDS_SCHEMA)

    # Get table columns
    cur.execute("PRAGMA table_info(mtg_cards)")
    tmp = cur.fetchall()
    cols = [t[1] for t in tmp]

    # Get the JSON card data
    all_cards = get_cards_json()

    # Iterate through the cards, putting their data into lists for the DB
    sql_v = [] #Individual card values
    sql_row_v = [] #Rows of cards
    for key in all_cards:
        for col in cols:
            sql_v.append(str(all_cards[key][col]) if col in all_cards[key] else None)
        sql_row_v.append(sql_v.copy())
        sql_v.clear()

    # Store the card data in the DB
    cur.executemany("INSERT INTO mtg_cards ({}) VALUES({}{})".format(",".join(cols), "?,"*(len(cols)-1), "?"), sql_row_v)
    db.commit()
    db.close()
