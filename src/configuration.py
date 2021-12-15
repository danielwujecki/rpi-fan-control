"""
This module provides the Config class to store the configuration tree

Furthermore utility functions to read and create a Config object
from commandline inputs and a YAML file are provided
"""

import os
import argparse


class Config(dict):
    """
    Fancy Configuration class
    Makes it possible to access a dictionary by member attributes.
    Example:
        cfg = Config({'a': 1, 'b': {'c': 2}})
        print(cfg.a) --> 1
        print(cfg.b.c) --> 2
    """
    @classmethod
    def _create_config_tree(cls, input_dict: dict):
        for key, val in input_dict.items():
            if isinstance(val, dict):
                input_dict[key] = cls(val)
        return input_dict

    def __init__(self, input_dict: dict):
        super().__init__(
            self._create_config_tree(input_dict)
        )

    def __getattr__(self, name):
        if name in self:
            return self[name]
        return None

    def __setattr__(self, key, val):
        if isinstance(val, dict):
            self[key] = Config(val)
        else:
            self[key] = val

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError(f"No such attribute: {name}")


def getcfg():
    """
    Asserts that config file is given as a command line parameter.
    config.yml is loaded and custom Config object is returned.
    """

    gpio_pin_default     = os.getenv("GPIO_PIN", "21")
    poll_intv_default    = os.getenv("POLL_INTERVAL", "5")
    temp_fan_on_default  = os.getenv("TEMP_FAN_ON", "55")
    temp_fan_off_default = os.getenv("TEMP_FAN_OFF", "50")

    parser = argparse.ArgumentParser(
        description="Raspberry Pi fan control daemon"
    )
    parser.add_argument(
        "-g", "--gpio-pin",
        type=int,
        default=gpio_pin_default,
        metavar="PIN_NUM",
        help="GPIO-Pin for fan control; defaults to 21"
    )
    parser.add_argument(
        "-p", "--poll-interval",
        type=int,
        default=poll_intv_default,
        metavar="POLL_INTV",
        help="Interval in seconds between temperatur checks; defaults to 5"
    )
    parser.add_argument(
        "-n", "--temp-fan-on",
        type=int,
        default=temp_fan_on_default,
        metavar="T_FAN_ON",
        help="Temperature in celcius to turn fan on; defaults to 55"
    )
    parser.add_argument(
        "-f", "--temp-fan-off",
        type=int,
        default=temp_fan_off_default,
        metavar="T_FAN_OFF",
        help="Temperature in celcius to turn fan off; defaults to 50"
    )
    cfg = Config(vars(parser.parse_args()))
    return cfg


if __name__ == "__main__":
    # Debugging
    config = getcfg()
    print(config)
