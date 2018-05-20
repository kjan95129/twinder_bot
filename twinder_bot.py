# twinder_bot.py

import re
import sqlite3
import socket
from time import sleep

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "twinder_bot"
PASS = "oauth:u55e0hl74cp4767wxo21tuvqcmmb1m"
CHAN = "#twinder_bot"
JOIN_CMD = "!join"
LEAVE_CMD = "!leave"
DB_NAME = "chat_server.db"
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

INSERT_USER_CMD = "INSERT INTO Users VALUES(NULL,\"{user}\")"
QUERY_USERS_CMD = "SELECT COUNT(*) FROM Users WHERE username=\"{user}\""

s = socket.socket()
s.connect((HOST, PORT))

s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

db = sqlite3.connect(DB_NAME)
c = db.cursor()

while True:
    response = s.recv(1024).decode("utf-8")

    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)

        if message.strip() == JOIN_CMD:
            c.execute(QUERY_USERS_CMD.format(user=username))
            user_exists = c.fetchone()[0]
            print("Joining chat")
            print(user_exists)

            if user_exists == 0:
                c.execute(INSERT_USER_CMD.format(user=username))
                # TODO: Check Unmatched table for username
                db.commit()
            elif user_exists == 1:
                print("User already exists")
            else:
                print("Probably throw an exception here")

        if message.strip() == LEAVE_CMD:
            print("Leaving chat")
        print(username + ": " + message)

    sleep(0.1)
