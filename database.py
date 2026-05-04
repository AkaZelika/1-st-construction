import sqlite3, os

def create_data():
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    users = """
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            city TEXT NOT NULL
        )
    """
    concerts = """
        CREATE TABLE IF NOT EXISTS Concerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            time TIME NOT NULL,
            city TEXT NOT NULL,
            location TEXT,
            count INTEGER
        )
    """ #date=YYYY-MM-DD; time=hh-mm-ss
    items = """
        CREATE TABLE IF NOT EXISTS Items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            descriptoin TEXT,
            count INTEGER
        )
    """
    type_ticket = """
        CREATE TABLE IF NOT EXISTS Type_ticket(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """
    carts = """
        CREATE TABLE IF NOT EXISTS Carts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id INTEGER,
            count INTEGER,
            FOREIGN KEY (user_id) REFERENCES Users (id),
            FOREIGN KEY (item_id) REFERENCES Items (id)
        )
    """
    ticket = """
        CREATE TABLE IF NOT EXISTS Ticket(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_id INTEGER,
            user_id INTEGER,
            concert_id INTEGER,
            FOREIGN KEY (type_id) REFERENCES Type_ticket (id),
            FOREIGN KEY (user_id) REFERENCES Users (id),
            FOREIGN KEY (concert_id) REFERENCES Concerts (id)
        )
    """
    codes = [users, concerts, items, type_ticket, carts, ticket]
    for code in codes:
        cur.execute(code)
        con.commit()

    con.close()

def add_concert(date, time, city, location, count=0):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("INSERT INTO Concerts (date, time, city, location, count) VALUES (?, ?, ?, ?, ?)", 
                (date, time, city, location, count))
    con.commit()
    con.close()

def get_concerts():
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    concerts = cur.execute("SELECT * FROM Concerts").fetchall()
    con.close()
    return concerts

def get_ticket(concert_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    ticket_info = cur.execute("SELECT * FROM Concerts WHERE id=?", (concert_id,)).fetchone()
    con.close()
    return ticket_info

def add_item(name, price, image="", description="", count=0):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("INSERT INTO Items (image, name, price, descriptoin, count) VALUES (?, ?, ?, ?, ?)", 
                (image, name, price, description, count))
    con.commit()
    con.close()

def get_items():
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    concerts = cur.execute("SELECT * FROM Items").fetchall()
    con.close()
    return concerts

def get_item(item_id, item_name):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    item_info = cur.execute("SELECT * FROM Items WHERE id=? AND name=?", (item_id, item_name)).fetchone()
    con.close()
    return item_info

def user_login(email, city):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("INSERT INTO Users (email, city) VALUES (?, ?)", (email, city))
    con.commit()
    con.close()

def get_user(email, info=""):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    user_acc = cur.execute(f"SELECT {info} FROM Users WHERE email=?", (email,)).fetchone()
    con.close()
    return user_acc

def buy_ticket(type_id, user_id, consert_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("INSERT INTO Ticket (type_id, user_id, consert_id) VALUES (?, ?, ?)", (type_id, user_id, consert_id))
    con.commit()
    con.close()

def buy_product(item_id, user_id="", count=1):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("INSERT INTO Carts (user_id, item_id, count) VALUES (?, ?, ?)", (user_id, item_id, count))
    con.commit()
    cur.execute("SELECT id FROM Carts WHERE user_id=? AND item_id=?", (user_id, item_id))
    product_id = cur.fetchone()
    con.close()
    return product_id[0]

def get_cart_product(cart_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("SELECT * FROM Carts WHERE id=?", (cart_id,))
    product_id = cur.fetchone()
    con.close()
    return product_id

def cart_update(id, count):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    if count > 0:
        cur.execute("UPDATE Carts SET count = ? WHERE id = ?", (count, id))
    else:
        cur.execute("DELETE Carts WHERE id = ?", (id,))
    con.commit()
    con.close()

def get_len_cart(user_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    id = cur.execute("SELECT id FROM Carts WHERE user_id=?", (user_id,)).fetchall()
    con.commit()
    con.close()
    return len(id)

def product_in_cart(cart_id, product_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    count = cur.execute("SELECT count FROM Carts WHERE id=? AND item_id=?", (cart_id, product_id)).fetchone()
    con.close()
    if count == None:
        return 0
    else:
        return count[0]

def delete_data():
    files = os.listdir("static/products")
    for file in files:
        os.remove("static/products/" + file)
    os.remove("data.bd")

if __name__ == "__main__":
    create_data()
    #add_concert(date="2026-04-15", time="15-30", city="Novosibirsk", location="Ул.Татьяны-Снежиной, 51, кв.52", count=10)
    #add_concert(date="04-25", time="15-00", city="Novosibirsk", location="Ул.Татьяны-Снежиной, 51, кв.52")
    print(get_concerts())
    if input("delete database? Y/N ") == "Y":
        delete_data()