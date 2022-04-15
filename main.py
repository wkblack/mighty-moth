# ⚠️ Only modify this file if you know what you're doing!

import socket
from bot import TicTacToeBot

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect("/tmp/zilch.sock")

    bot = None

    while True:
        split = bytes.decode(client.recv(2048), "utf-8").split(",", 2)
        channel = split[0]
        messageId = split[1]

        response = ""
        if channel == "init":
            data = split[2].split(",")
            bot = TicTacToeBot({
                "player": data[0],
                "color": data[1],
                "game_time_limit": int(data[2]),
                "turn_time_limit": int(data[3]),
            })
        elif channel == "move":
            data = list(map(
                lambda row: row.split(","),
                split[2].split("|")
            ))
            move = bot.move(data)
            response = str(move["x"]) + "," + str(move["y"])

        client.send((channel + "," + messageId +
                    "," + response).encode("utf-8"))
