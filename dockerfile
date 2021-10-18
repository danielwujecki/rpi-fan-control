FROM python:3.8.10
WORKDIR /usr/src/rpi-fan-control
RUN CFLAGS=-fcommon pip install --no-cache-dir RPi.GPIO
COPY src/cputemp.py src/rpi_fan_control.py ./
CMD [ "/usr/local/bin/python", "/usr/src/rpi-fan-control/rpi_fan_control.py" ]
