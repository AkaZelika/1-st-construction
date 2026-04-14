import sqlite3

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
    """
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


if __name__ == "__main__":
    create_data()