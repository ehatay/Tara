#!/usr/bin/env bash
echo "STARTING"
export THEIP=$(ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' | tail -1 | cut -d: -f2 | awk '{ print $1 }')
bash -c "roslaunch tara_app run.launch"
