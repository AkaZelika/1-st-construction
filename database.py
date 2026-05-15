import sqlite3, os

#Берет всю информацию об определенном предмете
def get_item(item_id, item_name):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    item_info = cur.execute("SELECT * FROM Items WHERE id=? AND name=?", (item_id, item_name)).fetchone()
    con.close()
    return item_info

# все продукты в корзине
def get_cart_product(cart_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("SELECT * FROM Carts WHERE id=?", (cart_id,))
    product_id = cur.fetchone()
    con.close()
    return product_id

#
def get_product_in_cart(cart_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    cur.execute("""SELECT Carts.item_id, Items.name, Items.image, Carts.count, Items.count, Items.price, Carts.id FROM Carts 
                    INNER JOIN Items 
                    ON Carts.item_id = Items.id
                    WHERE Carts.id=?
                    ORDER BY Carts.id DESC""", (int(cart_id),))
    product_info = cur.fetchone()
    print(product_info)
    con.close()
    return product_info

# обновить число продуктов в карзине
def cart_update(id, count):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    
    if count>0:
        cur.execute("UPDATE Carts SET count =? WHERE id =?", (count, id))
    else:
        cur.execute("DELETE Carts WHERE id = ?", (id,))
    con.commit()
    con.close()

#сколько продуктов в корзине
def get_len_cart(user_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    id = cur.execute("SELECT id FROM Carts WHERE user_id=?", (user_id,)).fetchall()
    con.commit()
    con.close()
    return len(id)

#сколько продукта в корзине
def product_in_cart(cart_id, product_id):
    con = sqlite3.connect("data.bd")
    cur = con.cursor()
    count = cur.execute("SELECT count FROM Carts WHERE id=? AND item_id=?", (cart_id, product_id)).fetchone()
    con.close()
    if count == None:
        return 0
    else:
        return count[0]

class Database:
    def __init__(self):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()

    def create(self):
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
                description TEXT,
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
            self.cur.execute(code)
            self.con.commit()

    def get_users(self, option="*"):
        accouts = self.cur.execute(f"SELECT {option} FROM Users").fetchall()
        return accouts
    
    def get_concerts(self, option="*"):
        concerts = self.cur.execute(f"SELECT {option} FROM Concerts ORDER BY date, time ASC").fetchall()
        return concerts
    
    def get_items(self, option="*"):
        items = self.cur.execute(f"SELECT {option} FROM Items").fetchall()
        return items
    
    def get_type_ticket(self, option="*"):
        types_ticket = self.cur.execute(f"SELECT {option} FROM Type_ticket").fetchall()
        return types_ticket
    
    def get_carts(self, option="*"):
        carts = self.cur.execute(f"SELECT {option} FROM Carts").fetchall()
        return carts
    
    def get_ticket(self, option="*"):
        ticket = self.cur.execute(f"SELECT {option} FROM Ticket").fetchall()
        return ticket
    
    def get_concert(self, id, option="*"):
        concert = self.cur.execute(f"SELECT {option} FROM Concerts WHERE id=?", (id,)).fetchone()
        return concert
    
    def get_item(self, id, option="*"):
        item = self.cur.execute(f"SELECT {option} FROM Items WHERE id=?", (id,)).fetchone()
        return item

    def delete_cart(self, id):
        self.cur.execute("DELETE FROM Carts WHERE id=?", (id,))
        self.con.commit()

class Users(Database):
    def __init__(self, email, city=""):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()
        self.email = email
        self.city = city
        self.id = self.cur.execute("SELECT id FROM Users WHERE email=?", (self.email,)).fetchone()
        if self.id:
            self.id = self.id[0]
    
    def add(self):
        if not self.id:
            self.cur.execute("INSERT INTO Users (email, city) VALUES (?, ?)", (self.email, self.city))
            self.con.commit()
            self.id = self.cur.execute("SELECT id FROM Users WHERE email=?", (self.email,)).fetchone()[0]
            return self.id
        else:
            return "user registred"
    
    def get(self, option="*"):
        accout = self.cur.execute(f"SELECT {option} FROM Users WHERE email=?", (self.email,)).fetchone()
        return accout
    
    def carts(self):
        cart = {}
        co = 1
        carts_id = self.cur.execute(f"SELECT id FROM Carts WHERE user_id=? ORDER BY id DESC", (self.id,)).fetchall()
        for id in carts_id:
            cart[str(co)] = id[0]
            co += 1
        return cart

class Concerts(Database):
    def __init__(self, date, time, city, location, count):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()
        self.date = date
        self.time = time
        self.city = city
        self.location = location
        self.count = count

    def add(self):
        self.cur.execute("INSERT INTO Concerts (date, time, city, location, count) VALUES (?, ?, ?, ?, ?)", 
                (self.date, self.time, self.city, self.location, self.count))
        self.con.commit()

    def delete(self):
        self.cur.execute()
        self.con.commit()

class Items(Database):
    def __init__(self, name="", price=10000, image="", description="", count=0, id=()):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()
        if id:
            self.id = id
        else:
            self.image = image
            self.name = name
            self.price = price
            self.description = description
            self.count = count

    def add(self):
        self.cur.execute("INSERT INTO Items (image, name, price, description, count) VALUES (?, ?, ?, ?, ?)", 
                (self.image, self.name, self.price, self.description, self.count))
        self.con.commit()

    def info(self):
        item = self.cur.execute("SELECT * FROM Items WHERE id=?", (self.id,)).fetchone()
        return item


    def delete(self):
        self.cur.execute()
        self.con.commit()

class Type_ticket(Database):
    def __init__(self, name):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()
        self.name = name

    def add(self):
        self.cur.execute("INSERT INTO Type_ticket (name) VALUES (?,)", (self.name,))
        self.con.commit()
    
    def delete(self):
        self.cur.execute()
        self.con.commit()

class Carts(Database):
    def __init__(self, item_id="NULL", user_id="NULL", count=1, id=()):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()
        if not id:
            self.user_id = user_id
            self.item_id = item_id
            self.count = count
            self.id = self.cur.execute("SELECT id FROM Carts WHERE user_id=? AND item_id=?", (self.user_id, self.item_id)).fetchone()
            if self.id:
                self.id = self.id[0]
        else:
            self.id = id
            data = self.cur.execute("SELECT user_id, item_id, count FROM Carts WHERE id=?", (self.id,)).fetchone()
            self.user_id = data[0]
            self.item_id = data[1]
            self.count = data[2]
    
    def add(self):
        self.cur.execute("INSERT INTO Carts (user_id, item_id, count) VALUES (?, ?, ?)", (self.user_id, self.item_id, self.count))
        self.con.commit()
        self.id = self.cur.execute("SELECT id FROM Carts WHERE user_id=? AND item_id=?", (self.user_id, self.item_id)).fetchone()[0]
        return self.id
    
    def get_info(self):
        self.cur.execute("""SELECT Carts.item_id, Items.name, Items.image, Carts.count, Items.count, Items.price, Carts.id FROM Carts 
                    INNER JOIN Items 
                    ON Carts.item_id = Items.id
                    WHERE Carts.id=?
                    ORDER BY Carts.id DESC""", (int(self.id),))
        info = self.cur.fetchone()
        return info
    
    def update(self, count):
        if count>0:
            self.cur.execute(f"UPDATE Carts SET count={count} WHERE id =?", (self.id,))
        else:
            self.cur.execute("DELETE FROM Carts WHERE id = ?", (self.id,))
        self.con.commit()

class Ticket(Database):
    def __init__(self, type_id, user_id, concert_id):
        self.bd_name = "data.bd"
        self.con = sqlite3.connect(self.bd_name)
        self.cur = self.con.cursor()
        self.type_id = type_id
        self.user_id = user_id
        self.concert_id = concert_id
    
    def add(self):
        self.cur.execute("INSERT INTO Ticket (type_id, user_id, consert_id) VALUES (?, ?, ?)", (self.type_id, self.user_id, self.consert_id))
        self.con.commit()
    
    def delete(self):
        self.cur.execute()
        self.con.commit()


if __name__ == "__main__":
    if os.path.exists("data.bd"):
        if input("delete database? Y/N ") == "Y":
            files = os.listdir("static/products")
            for file in files:
                os.remove("static/products/" + file)
            os.remove(os.path.abspath("data.bd"))
    else:
        bd = Database()
        bd.create()