import sqlite3
import json

def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class TicketsDB:

    def __init__(self):
        self.connection = sqlite3.connect("tickets.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        return

    def __del__(self):
        self.connection.close()
        return

    def createTicket(self, ent_name, ent_age, g_name, r_token):
        self.cursor.execute("INSERT INTO tickets (entrant_name, entrant_age, guest_name, random_token) VALUES (?, ?, ?, ?)", (ent_name, ent_age, g_name, r_token))
        self.connection.commit()
        return


    def getTickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        return self.cursor.fetchall()

def main():
    db = TicketsDB()
    rows = db.getTickets()
    print(json.dumps(rows))

if __name__ == "__main__":
    main()
