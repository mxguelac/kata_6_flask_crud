from datetime import date
import csv
import os
import sqlite3

CURRENCIES = ("EUR", "USD")

class Movement:
    def __init__(self, input_date, abstract, amount, currency, id = None):
        self.date = input_date
        self.id = id

        self.abstract = abstract
        self.amount = amount
        self.currency = currency

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = date.fromisoformat(value)
        if self._date > date.today():
            raise ValueError("date must be today or lower")
        
    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, value):
        self._amount = float(value)
        if self._amount == 0:
            raise ValueError("amount must be positive or negative")
        
    @property
    def currency(self):
        return self._currency
    
    @currency.setter
    def currency(self, value):
        self._currency = value
        if self._currency not in CURRENCIES:
            raise ValueError(f"currency must be in {CURRENCIES}")

    def __eq__(self, other):
        return self.date == other.date and self.abstract == other.abstract and self.amount == other.amount and self.currency == other.currency

    def __repr__(self):
        return f"Movimiento: {self.date} - {self.abstract} - {self.amount} {self.currency}"

class MovementDAOsqlite:
    def __init__(self, db_path):
        self.path = db_path

        query = """
        CREATE TABLE IF NOT EXISTS "movements" (
            "id"	INTEGER UNIQUE,
            "date"	TEXT NOT NULL,
            "abstract"	TEXT NOT NULL,
            "amount"	REAL NOT NULL,
            "currency"	TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        conn.close()

    def insert(self, movement):

        query = """
        INSERT INTO movements
               (date, abstract, amount, currency)
        VALUES (?, ?, ?, ?)
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date, movement.abstract,
                            movement.amount, movement.currency))
        conn.commit()
        conn.close()

    def get(self, id):
        query = """
        SELECT date, abstract, amount, currency, id
          FROM movements
         WHERE id = ?;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        conn.close()
        if res:
            return Movement(*res)

        
    def get_all(self):
        query = """
        SELECT date, abstract, amount, currency, id
          FROM movements
         ORDER by date;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        """
        lista = []
        for reg in res:
            lista.append(Movement(*reg))
        """

        lista = [Movement(*reg) for reg in res]

        conn.close()
        return lista

    def update(self, id, movement):
        query = """
        UPDATE movements
           SET date = ?, abstract = ?, amount = ?, currency = ?
         WHERE id = ?;
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date, movement.abstract, movement.amount, movement.currency, id))
        conn.commit()
        conn.close()






class MovementDAO:
    def __init__(self, file_path):
        self.path = file_path
        if not os.path.exists(self.path):
            f = open(file_path, "w")
            f.write("date,abstract,amount,currency\n")

    def insert(self, movement):
        f = open(self.path, "a", newline="")
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow([movement.date, movement.abstract, 
                         movement.amount, movement.currency])
        f.close()
        
    def all(self):
        # devolver una lista de Movements con todos los registros del fichero
        f = open(self.path, "r")
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        movements = []
        for register in reader:
            m = Movement(register["date"], register["abstract"], register["amount"], register["currency"])
            movements.append(m)
        return movements
    
    def get(self, pos):
        f = open(self.path, "r")
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        ix = float("-inf")
        for ix, register in enumerate(reader):
            if ix == pos:
                break

        if pos > ix:
            raise IndexError("movement don't exist")
        
        m = Movement(register["date"], register["abstract"], register["amount"], register["currency"])
        return m

    def update(self, pos, movement):
        f = open(self.path, "r")
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        regs = list(reader)
        fieldnames = reader.fieldnames
        f.close()
        new_name = "__movements__new.csv"
        f = open(new_name, "w", newline="")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(regs[:pos])
        writer.writerow({"date": movement.date, "abstract": movement.abstract, 
                         "amount": movement.amount, "currency": movement.currency})
        writer.writerows(regs[pos+1:])
        f.close()
        os.rename(new_name, self.path)