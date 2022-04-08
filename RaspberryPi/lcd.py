import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd


class LCD(characterlcd.Character_LCD_Mono):

    lcd_rs = digitalio.DigitalInOut(board.D22)
    lcd_en = digitalio.DigitalInOut(board.D17)
    lcd_d4 = digitalio.DigitalInOut(board.D7)
    lcd_d5 = digitalio.DigitalInOut(board.D24)
    lcd_d6 = digitalio.DigitalInOut(board.D23)
    lcd_d7 = digitalio.DigitalInOut(board.D18)

    lcd_columns = 16
    lcd_rows = 2

    def __init__(self):
        super().__init__(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            self.lcd_columns,
            self.lcd_rows,
            None,
            False,
        )
