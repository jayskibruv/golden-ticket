from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from ticketdb import TicketsDB
from http import cookies
import json
import random

class TicketHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods","POST, GET, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
        return

    def do_POST(self):
        self.load_cookie()

        if self.path == "/tickets":
            self.handleTicketCreate()
        else:
            self.handle404()

    def do_GET(self):
        self.load_cookie()

        if self.path == "/tickets":
            self.handleAllTickets()
        else:
            self.handle404()


    def end_headers(self):
        self.send_header("Access-Control-Allow-Credentials","true")
        self.send_header("Access-Control-Allow-Origin",self.headers["Origin"])
        BaseHTTPRequestHandler.end_headers(self)

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
            self.cookie["oompa"] = ""
            self.cookie["oompa"]["expires"] = 0
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def handleTicketCreate(self):
        length = self.headers['Content-Length']
        length = int(length)

        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)
        json_log = json.dumps(data)

        entrant_name = data["entrant_name"][0]
        entrant_age = data["entrant_age"][0]
        guest_name = data["guest_name"][0]
        random_token = random.randint(0,6)

        db = TicketsDB()
        if self.cookie:
            self.send_response(403)
            print("New ticket submission was attempted, but not allowed.")
            self.wfile.write(bytes("<h4>The Oompa Loompas have already received your ticket. Please try again tomorrow.</h4>","utf-8"))
        else:
            self.send_response(201)
            self.send_header("Content-Type", "application/x-www-form-urlencoded")
            db.createTicket(entrant_name, entrant_age, guest_name, random_token)
            self.cookie["oompa"] = "loompa"
            self.send_cookie()
            print("New Ticket Submitted: " + json_log)

        self.end_headers()
        return

    def handleAllTickets(self):

        self.send_response(200)
        self.send_header("Content-Type", "application/json")

        db = TicketsDB()
        tickets = db.getTickets()
        json_log = json.dumps(tickets)

        print("Jolly Ho! Here are all the tickets: ", json_log)
        self.end_headers()
        self.wfile.write(bytes(json_log, "utf-8"))

    def handle404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<h3>It seems that this resource has been lost in the chocolate pipes. An Oompa Loompa will be dispatched promptly to recover the artifact.</h3>","utf-8"))

    def handle403(self):
        self.send_response(403)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<h1>403: Forbidden</h1>","utf-8"))

def main():
	listen = ("127.0.0.1", 8080)
	server = HTTPServer(listen, TicketHandler)

	print("Listening...")
	server.serve_forever()

main()
