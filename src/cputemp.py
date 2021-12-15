#!/usr/bin/env python3

import os


def get():
    """
    Obtains the current CPU temperature.
    :returns: Current CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    result = -1.
    # The first line in this file holds the CPU temperature times 1000 as an integer.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp', encoding="utf-8") as f:
            line = f.readline().strip()
        if line.isdigit():
            result = float(line) / 1000
    return result


if __name__ == "__main__":
    output = f"Current CPU temperature is {get():.2f} degrees Celsius."
    print(output, flush=True)
