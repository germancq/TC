#!/bin/bash

#install visual studio code
sudo apt update
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install code

#install platformIO
sudo apt-get install python3-venv
code --install-extension platformio.platformio-ide

#install pip3
sudo apt install python3-pip

#install python packages
pip3 install --user pyserial
pip3 install --user matplotlib
pip3 install --user numpy

#uninstall brltty

sudo apt remove brltty
