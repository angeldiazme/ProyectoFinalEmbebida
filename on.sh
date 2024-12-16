#!/bin/bash
gpio -g mode 17 out
gpio -g write 17 0
sleep 5
gpio -g mode 17 out
gpio -g write 17 1
