import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import ast
import re

"""
Button:
     7: GPIO 4
     9: GROUND
RFID PINS:
    19: GPIO 10 (SPI0 MOSI)
    20: GROUND
    21: GPIO 9 (SPI0 MISO)
    22: GPIO 25
    23: GPIO 11 (SPI0 SCLK)
    24: GPIO 8 (SPI0 CS0)
    
passive Buzzer:
    14: GROUND
    16: (GPIO 23)
    
LED:
    33: GPIO 13
    35: GPIO 19 (SPI1 MISO)
    37: GPIO 26
    39: GROUND
"""

GPIO.setmode(GPIO.BCM)

# Button setup
Button_PIN = 4
GPIO.setup(Button_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Buzzer setup
Buzzer_PIN = 23
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial= GPIO.LOW)

# LED setup
LED_ROT = 19
LED_GRUEN = 26
LED_BLAU = 13
 
GPIO.setup(LED_ROT, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_GRUEN, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_BLAU, GPIO.OUT, initial= GPIO.LOW)


reader = SimpleMFRC522()

#if button pressed:
GPIO.output(Buzzer_PIN, GPIO.HIGH)
time.sleep(2)
GPIO.output(Buzzer_PIN,GPIO.LOW)

def getDirection(shortDir):
        if shortDir == "t":
            return "Top"
        elif shortDir == "tr":
            return "Top Right"
        elif shortDir == "r":
            return "Right"
        elif shortDir == "br":
            return "Bottom Right"
        elif shortDir == "b":
            return "Bottom"
        elif shortDir == "bl":
            return "Bottom Left"
        elif shortDir == "l":
            return "Left"
        elif shortDir == "tl":
            return "Top Left"
        else:
            return "Unknown Direction"

def getDistance(shortDist):
    splitDistString = re.split('(\d+)',shortDist)
    
    unit = "test"
    print(splitDistString)
    if splitDistString[2] == "cm":
        unit = "Centimeters"
        
    return splitDistString[1] + unit
        

def getParsedDirectionString(unparsedString):
    splitString = unparsedString.split()
    
    return getDistance(splitString[0]) + getDirection(splitString[1])

def playSound(voiceLine):
    tts = gTTS(voiceLine, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    song = AudioSegment.from_file(fp)
    play(song)


def smartClimb(null):
    print("You can now start climbing.")
    GPIO.output(LED_ROT,GPIO.LOW)
    GPIO.output(LED_GRUEN,GPIO.HIGH)
    GPIO.output(LED_BLAU,GPIO.LOW)
    try:
        id, text = reader.read()
        print(id)
        print(text)
        parsedText = ast.literal_eval(text)
        
        #playSound(parsedText["type"])
        directionString = getParsedDirectionString(parsedText["next"])
        playSound(parsedText["type"] + directionString)
        
        smartClimb(null)
        
    finally:
        GPIO.cleanup()

# When a signal is detected (falling signal edge) the output function is executed
GPIO.add_event_detect(Button_PIN, GPIO.FALLING, callback=smartClimb, bouncetime=100) 


print("SmartClimb system is running. Press the button once you want to start climbing!")

GPIO.output(LED_ROT,GPIO.LOW)
GPIO.output(LED_GRUEN,GPIO.LOW)
GPIO.output(LED_BLAU,GPIO.HIGH)
# main program loop
try:
    while True:
        time.sleep(1)
  
# clean up after the program is finished
except KeyboardInterrupt:
    GPIO.cleanup()

