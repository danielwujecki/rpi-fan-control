#!/usr/bin/env python3

import time
import signal
import logging
import RPi.GPIO as gpio

import cputemp


GPIO_PIN         = 21       # Number of GPIO pin to control the fan
POLL_INTERVAL    = 5        # How long to sleep between each cpu temp check
CPU_TEMP_FAN_ON  = 47       # Temperatur on which the fan is turned on
CPU_TEMP_FAN_OFF = 44       # Temperatur on which the fan is turned off

logger = logging.getLogger("rpifancontrol")


def configure_logging():
    fmt = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s - %(name)s: %(message)s",
        datefmt="%d-%m-%y %H:%M:%S"
    )
    ch = logging.StreamHandler()
    loglevel = logging.INFO
    ch.setLevel(loglevel)
    ch.setFormatter(fmt)
    rlogger = logging.getLogger("")
    rlogger.setLevel(loglevel)
    rlogger.addHandler(ch)


def sigterm_handler(run):
    """
    function called when a SIGTERM or SIGINT (ctrl-c) is received
    """
    logger.info("Received signal: exiting.")
    run.pop()


def check_cpu_temp(current_state=-1):
    """
    this checks the cpu temperatur once and turns the fan
    on or off, based on the temperatur thresholds
    """
    temp = cputemp.get()
    if temp >= CPU_TEMP_FAN_ON and current_state != 1:
        logger.debug("Fan on")
        current_state = 1
        gpio.output(GPIO_PIN, gpio.HIGH)
    elif temp <= CPU_TEMP_FAN_OFF and current_state != 0:
        logger.debug("Fan off")
        current_state = 0
        gpio.output(GPIO_PIN, gpio.LOW)
    return current_state


def main():
    """
    this registers signal handlers, initialize gpio pins
    and then continues with the main loop
    """
    assert CPU_TEMP_FAN_OFF <= CPU_TEMP_FAN_ON

    configure_logging()

    gpio.setmode(gpio.BCM)
    gpio.setup(GPIO_PIN, gpio.OUT)
    gpio.output(GPIO_PIN, gpio.LOW)
    state = 0

    run = [ True ]
    signal.signal(signal.SIGTERM, lambda *_: sigterm_handler(run))
    signal.signal(signal.SIGINT, lambda *_: sigterm_handler(run))

    logger.info("Start main loop.")
    while run:
        state = check_cpu_temp(current_state=state)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
