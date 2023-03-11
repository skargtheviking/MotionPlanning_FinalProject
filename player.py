from importlib.resources import path
from pickle import FALSE, NONE
import numpy as np
import matplotlib.pyplot as plotter
from math import pi
from collisions import PolygonEnvironment
import time
import random


class player:
    '''
    Class to define the players and actions
    '''
    def __init__(self, state, parent=None):
            self.name = ""
            self.image = self.name+".jpg"
            self.Strength = 3
            self.Wisdom = 3
            self.Agility - 3
            self.Total_Actions = 3
            self.Currect_Actions = Total_Actions
            self.Red_token