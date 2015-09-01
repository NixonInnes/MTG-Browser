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

#What even am I doing...
class Table(object):
    def __init__(self, sql, name, schema):
        self.sql = sql
        self.do(schema)
        self.set_name(name)
        self.set_cols()

    def get_sql_desc(self):
        db = sqlite3.connect(self.sql)
        cur = db.cursor()
        cur.execute("SELECT * FROM sqlite_master")
        master = cur.fetchall()
        db.disconnect()
        return master

    def set_name(self, name):
        tables = [t[1] for t in get_sql_master()]
        if name in tables:
            self.name = name
        else:
            raise Exception("table name does not match schema")

    def set_cols(self):
        tmp = self.get("PRAGMA table_info({})".format(self.name))
        self.cols = [t[1] for t in tmp]
        
        
    def do(self, query):
        try:
            db = sqlite3.connect(self.sql)
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            db.disconnect()
        except Exception as e:
            return e

    def get(self, query):
        try:
            db = sqlite3.connect(self.sql)
            cur = db.cursor()
            cur.execute(query)
            r = cur.fetchall()
            db.commit()
            db.disconnect()
            return r
        except Exception as e:
            return e
    
    def add_row(self, data):
        cols = len(data)
        self.do("INSERT INTO {}")
    

def create_users_table():
    # Connect to DB
    db = sqlite3.connect(DB_FILENAME)
    cur = db.cursor()

    # Drop the exising users table
    cur.execute("DROP TABLE IF EXISTS users")
    # Create a fresh table
    cur.execute(USERS_SCHEMA)

    db.commit()
    db.close()

def add_user(username, password):
    db = sqlite3.connect(DB_FILENAME)
    cur = db.cursor()

    cur.execute("INSERT INTO users name, password

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
