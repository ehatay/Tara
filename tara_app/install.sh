#!/usr/bin/env bash
sudo mv tara.service /lib/systemd/system/tara.service
sudo systemctl enable tara.service
sudo reboot
