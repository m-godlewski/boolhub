#!/bin/sh

influx bucket create -n network -o boolhub -r 0
influx bucket create -n air -o boolhub -r 0
influx bucket create -n health -o boolhub -r 0