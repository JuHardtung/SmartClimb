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
    """Takes unparsed directiuon string and parses it to a parsed direction String for later TTS"""
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
    """Takes unparsed distance string and returns a parsed string with full distance unit for later TTS"""
    splitDistString = re.split('(\d+)',shortDist)
    
    unit = "Centimeters"
    if splitDistString[2] == "cm":
        unit = "Centimeters"
    elif splitDistString[2] == "in":
        unit = "Inches"
        
    return splitDistString[1] + unit
        

def getParsedDirectionString(unparsedString):
    """Takes unparsed String data and parses it to proper distance + direction for later TTS """
    splitString = unparsedString.split()
    
    return getDistance(splitString[0]) + getDirection(splitString[1])

def playSound(voiceLine):
    """Reads a text string out loud with google text to speech (gTTS)"""
    tts = gTTS(voiceLine, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    song = AudioSegment.from_file(fp)
    play(song)



NEXT_HOLD_NUM = 1

def smartClimb(null):
    global NEXT_HOLD_NUM
    """The main climbing loop"""
    print("You can now start climbing.")
    
    #show green status LED to show that "climbing mode" is activated
    GPIO.output(LED_ROT,GPIO.LOW)
    GPIO.output(LED_GRUEN,GPIO.HIGH)
    GPIO.output(LED_BLAU,GPIO.LOW)
        
    try:
        id, text = reader.read()
        
        parsedText = ast.literal_eval(text)
        
        if (parsedText["num"] == 999):
            playSound("You have reached the top! WOoow you are great")
            return
            
        directionString = getParsedDirectionString(parsedText["next"])
        
        if (parsedText["num"] < NEXT_HOLD_NUM):
            print("Already used that hold")
            playSound("Already used that hold")
            smartClimb(null)
            
        elif (parsedText["num"] > NEXT_HOLD_NUM):
            print("You skipped a hold but you can just keep climbing")
            playSound("You skipped a hold but you can just keep climbing")
            playSound(parsedText["type"] + directionString)
            
        elif (parsedText["num"] == NEXT_HOLD_NUM):        
            playSound(parsedText["type"] + directionString)
        
        NEXT_HOLD_NUM = NEXT_HOLD_NUM + 1
        smartClimb(null)
        
    finally:
        GPIO.cleanup()

# When the button is pressed, start "climbing mode"
GPIO.add_event_detect(Button_PIN, GPIO.FALLING, callback=smartClimb, bouncetime=100) 


print("SmartClimb system is running. Press the button once you want to start climbing!")

# show blue status LED to show that the program is running
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
