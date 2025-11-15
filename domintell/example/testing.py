import time
import logging
import sys
import domintell

def _on_message(message):
    print(">>> RECEIVED:", message)
    print(">>> RECEIVED JSON", message.to_json())

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Your controller address
HOST = "192.168.1.55:17481"

controller = domintell.Controller(HOST)
controller.subscribe(_on_message)

logging.info("LOGIN (no password)")
controller.login('LOGIN')   # no password

time.sleep(3)

#logging.info("Start scan")
#controller.scan(None)

# Wait long enough for PBL to send T/U temperature updates
logging.info("Listening...")
time.sleep(120)

controller.stop()
