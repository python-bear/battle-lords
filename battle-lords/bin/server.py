import socket
from _thread import *
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 8421

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

next_id = "0"
last_msgs = [None, None]

"""
    MESSAGE TYPES:
        00 = error
        10 = special
            11 = empty message
            12 = repeat last message
        20 = update
            21 = update piece positions
        30 = setup
            31 = map data
        40 =
        50 =
        60 =
        70 =
        80 =
        90 = disconnect
            91 = requested disconnect from client
            92 = accepted disconnect from server
"""


def client_connection(conn):
    global next_id, last_msgs

    conn.send(str.encode(next_id))
    if next_id == "0":
        next_id = "1"
    else:
        next_id = "0"

    while True:
        try:
            data = conn.recv(2048)
            message = data.decode("utf-8")
            print("Received: " + message)
            arguments = message.split("|")
            player_id = int(arguments[0])
            msg_type = int(arguments[1])

            if not data or msg_type == 91:
                conn.send(str.encode("-1|92|goodbye"))
                break
            else:
                last_msgs[player_id] = message

                other_player_id = 1 if player_id == 0 else 0

                message = last_msgs[other_player_id]
                message = message if message is not None else f"{player_id}|11|"
                print("Sending: " + message)

            conn.sendall(str.encode(message))
        except:
            break

    print("Connection Closed")
    conn.close()


s.settimeout(5)

try:
    while True:
        try:
            connection, address = s.accept()
            print("Connected to: ", address)

            start_new_thread(client_connection, (connection,))

        except socket.timeout:
            pass

except KeyboardInterrupt:
    print("Server Shutdown")

    s.close()
    sys.exit()
