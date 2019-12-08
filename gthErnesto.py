#!/usr/bin/python3

# Ernesto Martinez
# Minimax Search Alpha-Beta Prunning
# To play vs Gothello client.

import random
import sys

import gthclient

me = sys.argv[1]
opp = gthclient.opponent(me)

client = gthclient.GthClient(me, "localhost", 0)

print("working")