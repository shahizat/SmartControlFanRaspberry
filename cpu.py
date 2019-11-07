import RPi.GPIO as GPIO # Import a GPIO library
import sys # Import libraries for exception handling
from urllib import request # Import a library for working with URLs
from re import findall # Import a regex library
from time import sleep #Import a library to work with time
from subprocess import check_output # Import the library for working with subprocesses
myAPI = 'UNYFNTJUP797NRF7' # Enter Your API key here
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI # URL where we will send the data, Don't change it

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode()    # Perform temperature request
    temp = float(findall('\d+\.\d+', temp)[0])                   # Using regular expression, we get the temperature value from command line
    return(temp)
try:
    GPIO.setwarnings(False)                 # Disable GPIO warnings
    tempOn = 40                             # Turn on fan, when CPU temperature reaches 40degC
    controlPin = 14                         # Control GPIO 
    pinState = False                        # Actual state of fan
    GPIO.setmode(GPIO.BCM)                  # Set numbering system to BCM
    GPIO.setup(controlPin, GPIO.OUT, initial=0) # Set control GPIO to OUTPUT mode
    while True:
        temp = get_temp()
        if temp >= tempOn and not pinState or temp =< tempOn - 10 and pinState:
                pinState = not pinState         # Change the pin status 
                GPIO.output(controlPin, pinState) # Set a new status for the control pin
        conn = request.urlopen(baseURL + '&field1=%s' % (temp))
        print(str(temp) + "  " + str(pinState))
        print(conn.read())
        conn.close()
        sleep(1)
except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")            # Exit the program by pressing Ctrl + C
except:
    print("Other Exception")                # Other exceptions
    print("--- Start Exception Data:")
    traceback.print_exc(limit=2, file=sys.stdout) 
    print("--- End Exception Data:")
finally:
    print("CleanUp")                       
    GPIO.cleanup()                          # Return the pins state to their original state
    print("End of program")              

