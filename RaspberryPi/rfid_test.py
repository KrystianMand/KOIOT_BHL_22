#!/usr/bin/env python3

from email.base64mime import header_encode
import RPi.GPIO as GPIO
from lcd import LCD
from mfrc522 import SimpleMFRC522
import requests
from time import sleep
import json
from gpiozero import Button

PLACEID = 1
POSTURI = "http://192.168.43.145:5000/"


class Visitor:
    def __init__(self, is_visited, name, surname, points) -> None:
        self.name = name
        self.surname = surname
        self.points = points


if __name__ == "__main__":
    lcd = LCD()
    lcd.clear
    reader = SimpleMFRC522()
    button = Button(5)

    while True:
        lcd.message = "Przyloz karte"
        rfid, text = reader.read()
        personId = str(rfid)
        print(personId)
        lcd.clear()
        lcd.message = str(rfid)
        # response = requests.post(
        #     POSTURI + "visit", json={"place_id": PLACEID, "person_id": personId}
        # )
        respDict = json.loads(
            '{"is_visited": true,"name": "Marian","surname": "Chleb","points": -1}'
        )  # json.loads(response.content.decode())

        visitor = Visitor(**respDict)
        hello_msg = f"Witaj {visitor.name} {visitor.surname}"
        lcd.message = hello_msg
        sleep(2)
        for i in range(len(hello_msg)-16):
            lcd.move_left()
            sleep(0.5)
        sleep(1)
        lcd.clear()
        points_msg = f"Masz {visitor.points} punktow"
        lcd.message = points_msg
        sleep(2)
        lcd.clear()
        play_msg = "Chcesz zagrac w gre?"
        lcd.message = play_msg
        sleep(1)

        for i in range(len(play_msg) - 16):
            lcd.move_left()
            sleep(0.5)

        if button.wait_for_press(timeout=5):
            lcd.clear()
            lcd.message = "2 + 2 = ?"
            print("The button was pressed!")
        else:
            print("Thanks!")
        # if response.status_code == 200:
        #     print(response.content.decode())
        #     visitor = Visitor(**respDict)
        #     lcd.message = f"Witaj {visitor.name}"
        #     lcd.cursor_position(0, 1)
        #     play_msg = "Chcesz zagrac w gre?"
        #     lcd.message = play_msg
        #     sleep(1)

        #     for i in range(len(play_msg)):
        #         lcd.move_left()
        #         sleep(0.5)

        #     if button.wait_for_press(timeout=5):
        #         print("The button was pressed!")
        #     else:
        #         print("Thanks!")

        # else:
        #     lcd.clear()
        #     lcd.message = "error"

        sleep(5)
        lcd.clear()
