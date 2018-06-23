#!/bin/bash

scp install.sh setup.py pi@192.168.0.20:/Destination

scp co2_hass.py pi@192.168.0.20:/Destination

scp co2_hass.py pi@192.168.0.20:/Destination
cd CO2

scp __init__.py bluepy_back.py sensor_co2.py sensor_connection.py pi@192.168.0.20:/Destination

cd ../test/unit

scp test_application.py unit_test_runner.py unit_sensor_connection.py unit_sensor_co2.py mocker.py unit_bluepy_back.py __init__.py pi@192.168.0.20:/Destinatnion
cd ../integration

scp integ_sensor_co2.py pi@192.168.0.20:/Destination
