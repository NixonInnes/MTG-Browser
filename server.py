import sqlite3 as sql

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import config

app = Flask(__name__)
app.config.from_object(config.Debug)

def connect_db():
    return sql.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute("SELECT * FROM mtg_cards")
    cols = [col[0] for col in cur.description]
    rows = cur.fetchall()
    entry = {}
    entries = []
    for row in rows:
        for col in cols:
            entry[col] = row[cols.index(col)]
        entries.append(entry.copy())
    return render_template('show_entries.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if app.config['DEBUG'] is True:
            if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
                error = "Invalid username or password"
            else:
                session['logged_in'] = True
                flash('You are now logged in')
                return redirect(url_for('show_entries'))
        else:
            pass #TODO: Create user database & login function
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('show_entries'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sql_pre = "SELECT * FROM mtg_cards WHERE "
        sql_q = []
        sql_v = []
        sql_q.append("name LIKE ?")
        sql_v.append("%"+request.form['name_search']+"%")
        sql_q.append("type LIKE ?")
        sql_v.append("%"+request.form['type_search']+"%")
        if getattr(request.form, 'cmc_search'):
            sql_q.append("cmc <= ?")
            sql_v.append(request.form['cmc_search'])
        sql_q.append("text LIKE ?")
        sql_v.append("%"+request.form['text_search']+"%")
        sql_q = sql_pre + " AND ".join(sql_q)
        cur = g.db.execute(sql_q, sql_v)
        cols = [col[0] for col in cur.description]
        rows = cur.fetchall()
        entry = {}
        entries = []
        for row in rows:
            for col in cols:
                entry[col] = row[cols.index(col)]
            entries.append(entry.copy())
        return render_template('show_entries.html', entries=entries)
    return render_template('show_entries.html', entries=None)


if __name__ == '__main__':
    app.run()