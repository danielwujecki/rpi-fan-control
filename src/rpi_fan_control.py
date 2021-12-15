#!/usr/bin/env python3

import time
import signal
import logging
import RPi.GPIO as gpio

import cputemp
import configuration


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


def sigterm_handler(run: list, gpio_pin: int):
    """
    function called when a SIGTERM or SIGINT (ctrl-c) is received
    """
    logger.info("Received signal: exiting.")
    gpio.output(gpio_pin, gpio.LOW)
    run.pop()


def check_cpu_temp(cfg: configuration.Config, current_state=-1):
    """
    this checks the cpu temperatur once and turns the fan
    on or off, based on the temperatur thresholds
    """
    temp = cputemp.get()
    if temp >= cfg.temp_fan_on and current_state != 1:
        logger.debug("Fan on")
        current_state = 1
        gpio.output(cfg.gpio_pin, gpio.HIGH)
    elif temp <= cfg.temp_fan_off and current_state != 0:
        logger.debug("Fan off")
        current_state = 0
        gpio.output(cfg.gpio_pin, gpio.LOW)
    return current_state


def main():
    """
    this registers signal handlers, initialize gpio pins
    and then continues with the main loop
    """
    cfg = configuration.getcfg()
    assert cfg.temp_fan_off <= cfg.temp_fan_on

    configure_logging()
    logger.info(f"Starting with: {cfg}")

    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(cfg.gpio_pin, gpio.OUT)
    gpio.output(cfg.gpio_pin, gpio.LOW)
    state = 0

    run = [ True ]
    signal.signal(signal.SIGINT, lambda *_: sigterm_handler(run, cfg.gpio_pin))
    signal.signal(signal.SIGTERM, lambda *_: sigterm_handler(run, cfg.gpio_pin))

    logger.info("Start main loop.")
    while run:
        state = check_cpu_temp(cfg, current_state=state)
        time.sleep(cfg.poll_interval)


if __name__ == "__main__":
    main()
