#!/usr/bin/env python3

import sys
import time
import signal
import RPi.GPIO as gpio

import cputemp


GPIO_PIN         = 21       # Number of GPIO pin to control the fan
SLEEP_TIME       = 5        # How long to sleep between each cpu temp check
CPU_TEMP_FAN_ON  = 45       # Temperatur on which the fan is turned on
CPU_TEMP_FAN_OFF = 42       # Temperatur on which the fan is turned off


def sigterm_handler(*_):
    """
    function called when a SIGTERM or SIGINT (ctrl-c) is received
    """
    print("Received signal: exiting.")
    sys.exit(0)


def check_cpu_temp(current_state="unknown"):
    """
    this checks the cpu temperatur once and turns the fan
    on or off, based on the temperatur thresholds
    """
    temp = cputemp.get_cpu_temp()
    if temp >= CPU_TEMP_FAN_ON and current_state != "on":
        print("Fan on")
        current_state = "on"
        gpio.output(GPIO_PIN, gpio.HIGH)
    elif temp <= CPU_TEMP_FAN_OFF and current_state != "off":
        print("Fan off")
        current_state = "off"
        gpio.output(GPIO_PIN, gpio.LOW)
    return current_state


def main():
    """
    this registers signal handlers, initialize gpio pins
    and then continues with the main loop
    """
    assert CPU_TEMP_FAN_OFF <= CPU_TEMP_FAN_ON

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    gpio.setmode(gpio.BCM)
    gpio.setup(GPIO_PIN, gpio.OUT)
    gpio.output(GPIO_PIN, gpio.LOW)
    state = "off"

    print("Start main loop.")
    while True:
        state = check_cpu_temp(current_state=state)
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
