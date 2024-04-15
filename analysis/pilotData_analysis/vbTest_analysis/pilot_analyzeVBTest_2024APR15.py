import scipy.io
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog

setPairings = scipy.io.loadmat('setPairings2.mat')
print(setPairings) # [duration1, duration 2, 1=Left 0=Right] TODO: double check L/R with switch down

