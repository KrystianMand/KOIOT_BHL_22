#!/usr/bin/env python3

import RPi.GPIO as GPIO
from lcd import LCD
from mfrc522 import SimpleMFRC522
import requests
from time import sleep
import json

PLACEID = 1
POSTURI = "http://192.168.43.145:5000/"


class Visitor:
    def __init__(self, name, surname, points) -> None:
        self.name = name
        self.surname = surname
        self.points = points


if __name__ == "__main__":
    lcd = LCD()
    lcd.clear
    reader = SimpleMFRC522()

    while True:
        lcd.message = "Przyloz karte"
        rfid, text = reader.read()
        personId = str(rfid)
        lcd.clear()
        lcd.message = str(rfid)
        response = requests.post(
            POSTURI + "visit", json={"place_id": PLACEID, "person_id": personId}
        )
        if response.status_code == 200:
            print(response.content.decode())
            respDict = json.loads(response.content.decode())
            visitor = Visitor(**respDict)
            lcd.cursor_position(0, 1)
            lcd.message = f"Witaj {visitor.name}"

        sleep(1)
