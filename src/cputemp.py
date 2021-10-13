#!/usr/bin/env python3

import os


def main():
    """
    Print the current CPU temperature.
    """
    print('Current CPU temperature is {:.2f} degrees Celsius.'.format(get_cpu_temp()))


def get_cpu_temp():
    """
    Obtains the current CPU temperature.
    :returns: Current CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    result = 0.0
    # The first line in this file holds the CPU temperature times 1000 as an integer.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        if line.isdigit():
            result = float(line) / 1000
    return result


if __name__ == "__main__":
    main()
