from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Database setup
def init_db():
    conn = sqlite3.connect("bus.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS buses
                 (id INTEGER PRIMARY KEY, name TEXT, source TEXT, destination TEXT, seats INT, fare REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY, bus_id INT, passenger TEXT, seat_no INT, date TEXT)''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    source = request.form["source"]
    destination = request.form["destination"]
    conn = sqlite3.connect("bus.db")
    c = conn.cursor()
    c.execute("SELECT * FROM buses WHERE source=? AND destination=?", (source, destination))
    buses = c.fetchall()
    conn.close()
    return render_template("search.html", buses=buses)

@app.route("/book/<int:bus_id>", methods=["GET", "POST"])
def book(bus_id):
    if request.method == "POST":
        passenger = request.form["passenger"]
        seat_no = request.form["seat_no"]
        date = request.form["date"]
        conn = sqlite3.connect("bus.db")
        c = conn.cursor()
        c.execute("INSERT INTO bookings (bus_id, passenger, seat_no, date) VALUES (?, ?, ?, ?)",
                  (bus_id, passenger, seat_no, date))
        conn.commit()
        conn.close()
        return "✅ Booking Confirmed!"
    return render_template("book.html", bus_id=bus_id)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        source = request.form["source"]
        destination = request.form["destination"]
        seats = request.form["seats"]
        fare = request.form["fare"]
        conn = sqlite3.connect("bus.db")
        c = conn.cursor()
        c.execute("INSERT INTO buses (name, source, destination, seats, fare) VALUES (?, ?, ?, ?, ?)",
                  (name, source, destination, seats, fare))
        conn.commit()
        conn.close()
    return render_template("admin.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

