from flask import Flask, render_template
import sqlite3 as sql

main = Flask(__name__)

def get():
    y = sql.connect("data.db")
    x = y.cursor()
    return (x, y)
def init():
    (x, y) = get()
    x.execute("DROP TABLE IF EXISTS prod")
    x.execute("CREATE TABLE prod (name TEXT, PTH TEXT, pri INTEGER, st INTEGER)")
    x.execute("""INSERT INTO prod (name, PTH, pri, st) VALUES \
        ('Console', 'images/console.jpg', 69999, 0), ('Desktop', 'images/desktop.jpg', 110000, 10), ('Laptop', 'images/laptop.jpg', 180000, 3), \
        ('Phone', 'images/phone.png', 84999, 50), \
        ('TV', 'images/tv.png', 225049, 1)""")
    x.execute("DROP TABLE IF EXISTS tr")
    x.execute("CREATE TABLE tr (timestamp TEXT, productid INTEGER, value INTEGER)")
    y.commit()
@main.route("/")
def home():
    (x, y) = get()
    x.execute("SELECT rowid, * FROM prod")
    z = x.fetchall()
    i = []
    for y in z:
        i.append({"a":    y[0],"b":  y[1], "c":   "/static/%s" % (y[2]), "d": "$%.2f" % (y[3]/100.0), "e": "%d left" % (y[4]),})
    x.execute("SELECT SUM(value) FROM tr")
    result = x.fetchone()[0]
    cost = 0
    if result:
        cost = result / 100.0
    return render_template("index.html", x = i, y = cost)
@main.route("/buy/<prid>")
def buy(prid):
    (x, y) = get()
    x.execute("SELECT rowid, pri, st FROM prod WHERE rowid = ?", (prid,))
    result = x.fetchone()
    (rowid, pri, st) = result
    if st <= 0:
        return render_template("load.html", m = "Not Enough Stock!")
    x.execute("UPDATE prod SET st = st - 1 WHERE rowid = ?", (prid,))
    y.commit()
    return render_template("load.html", m ="Purchase Made!")
@main.route("/reset")
def reset():
    init()
    return render_template("load.html", m ="Store Reset")
if __name__ == '__main__':
    init()
    main.run(debug = True)