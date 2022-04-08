#!/usr/bin/env python

import RPi.GPIO as GPIO
from lcd import LCD
from mfrc522 import SimpleMFRC522


def writeData(reader):
    try:
        text = input("New data:")
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
    finally:
        GPIO.cleanup()


def readData(reader):
    try:
        id, text = reader.read()
        print(id)
        print(text)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    lcd = LCD()
    lcd.clear
    reader = SimpleMFRC522()
    id, text = reader.read()
    lcd.message = str(id)
