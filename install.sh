#!/bin/bash

echo "===Installing pip3==="
sudo apt-get install python3-pip

echo "===Installing pyglet, tkinter and fastnumbers==="
sudo pip3 install pyglet
sudo pip3 install fastnumbers
sudo apt-get install python3-tk
sudo apt-get install python3-networkx