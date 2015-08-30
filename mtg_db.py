import sqlite3
import requests
import os

BASIC_LANDS = (
    'plains',
    'island',
    'swamp',
    'mountain',
    'forest')

DB_FILENAME = "data/mtg.sqlite"

CARDS_DB_COLS = (
    'layout',
    'colors',
    'power',
    'name',
    'subtypes',
    'types',
    'cmc',
    'manaCost',
    'imageName',
    'text',
    'type',
    'toughness',
    'supertypes',
    'names',
    'starter',
    'hand',
    'life',
    'loyalty')

SETS_DB_COLS = (
    'code',
    'magicCardsInfoCode',
    'border',
    'releaseDate',
    'type',
    'magicRaritiesCodes',
    'name',
    'cards',
    'booster',
    'languagesPrinted',
    'block',
    'gathererCode',
    'onlineOnly',
    'oldCode')

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

def get_card(card_name):
    card = dict()
    if str(card_name).lower() in BASIC_LANDS:
        for col in CARDS_DB_COLS:
            card[col] = 'NaN'
        card['layout'] = 'normal'
        card['name'] = str(card_name).title()
        card['types'] = ['Land']
        card['type'] = 'Land'
        return card
    else:
        search = card_search(card_name)
        if len(search) == 1:
            for col in CARDS_DB_COLS:
                card[col] = search[0][len(card)]
            return card
        else:
            return None

def get_sets_json():
    try:
        sets = requests.get('http://mtgjson.com/json/AllSets.json').json()
        return sets
    except:
        return {}

def get_cards_json():
    try:
        cards = requests.get('http://mtgjson.com/json/AllCards.json').json()
        return cards
    except:
        return {}

def create_mtg_table():
    while True:
        if not os.path.isfile(DB_FILENAME):
            db = sqlite3.connect(DB_FILENAME)
            cur = db.cursor()
            cur.execute('''
                CREATE TABLE mtg_sets(
                    code TEXT,
                    magicCardsInfoCode TEXT,
                    border TEXT,
                    releaseDate DATE,
                    type TEXT,
                    magicRaritiesCodes TEXT,
                    name TEXT,
                    cards TEXT,
                    booster TEXT,
                    languagesPrinted TEXT,
                    block TEXT,
                    gathererCode TEXT,
                    onlineOnly TEXT,
                    oldCode TEXT)
                ''')
            cur.execute('''
                CREATE TABLE mtg_cards(
                    layout TEXT,
                    colors TEXT,
                    power TEXT,
                    name TEXT,
                    subtypes TEXT,
                    types TEXT,
                    cmc INT,
                    manaCost TEXT,
                    imageName TEXT,
                    text TEXT,
                    type TEXT,
                    toughness TEXT,
                    supertypes TEXT,
                    names TEXT,
                    starter TEXT,
                    hand TEXT,
                    life TEXT,
                    loyalty TEXT)
                ''')
            db.commit()
            db.close()
            break
        else:
            usr = input("mtg.sqlite already exists, delete it? [Y/N]")
            if usr.lower() == 'n':
                break
            elif usr.lower() == 'y':
                os.remove(DB_FILENAME)

def populate_cards_table():
    if not os.path.isfile(DB_FILENAME):
        create_mtg_table()
    db = sqlite3.connect(DB_FILENAME)
    cur = db.cursor()
    all_cards = get_cards_json()
    for key in all_cards:
        table_list = list()
        for header in CARDS_DB_COLS:
            table_list.append(str(all_cards[key][header]) if header in all_cards[key] else None)
        cur.execute('''
            INSERT INTO mtg_cards(
                layout,
                colors,
                power,
                name,
                subtypes,
                types,
                cmc,
                manaCost,
                imageName,
                text,
                type,
                toughness,
                supertypes,
                names,
                starter,
                hand,
                life,
                loyalty)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',table_list)
    db.commit()
    db.close()

def populate_sets_table():
    if not os.path.isfile(DB_FILENAME):
        create_mtg_table()

    db = sqlite3.connect(DB_FILENAME)
    cur = db.cursor()
    all_sets = get_sets_json()
    for key in all_sets:
        table_list = list()
        for header in SETS_DB_COLS:
            table_list.append(str(all_sets[key][header]) if header in all_sets[key] else None)
        cur.execute('''
            INSERT INTO mtg_sets(
                code,
                magicCardsInfoCode,
                border,
                releaseDate,
                type,
                magicRaritiesCodes,
                name,
                cards,
                booster,
                languagesPrinted,
                block,
                gathererCode,
                onlineOnly,
                oldCode)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',table_list)
    db.commit()
    db.close()
