import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import filedialog

# load dir
np.set_printoptions(suppress=True) # suppress scientific notation
root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory()

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import filedialog

# load dir
np.set_printoptions(suppress=True) # suppress scientific notation
root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory()

def calc_regression(x, y):
    slope, intercept, r, p, _ = stats.linregress(x, y)
    return slope, intercept, r, p

# import data
    # i. load inputs as numpy arrays
        # 1. resp (36x6; probably want RT4 resp)
in_resp_file = os.path.normpath(os.path.join(directory, 'features\\in_resp.csv'))
in_resp = np.genfromtxt(in_resp_file, delimiter=',')
in_resp = in_resp[1:]

        # 2. proprio
in_proprio_file = os.path.normpath(os.path.join(directory, 'features\\in_proprio_RMSE.csv'))
in_proprio = np.genfromtxt(in_proprio_file, delimiter=',')
in_proprio = in_proprio[1:]

        # 3. bFPA
in_bFPA_file = os.path.normpath(os.path.join(directory, 'features\\in_bFPA.csv'))
in_bFPA = np.genfromtxt(in_bFPA_file, delimiter=',')
in_bFPA = in_bFPA[1:]

        # 4. vbtest # TODO: discuss whether this should be included at all
in_vbtest_file = os.path.normpath(os.path.join(directory, 'features\\in_vbtest.csv'))
in_vbtest = np.genfromtxt(in_vbtest_file, delimiter=',')

        # 5. ROM in
        # NOTE: this is saved as negative, because it's toe-in; I switch the sign when assembling the array 
in_ROM_in_file = os.path.normpath(os.path.join(directory, 'features\\in_ROM_in.csv'))
in_ROM_in = np.genfromtxt(in_ROM_in_file, delimiter=',')  
in_ROM_in = in_ROM_in[1:]  

        # 6. ROM out
in_ROM_out_file = os.path.normpath(os.path.join(directory, 'features\\in_ROM_out.csv'))
in_ROM_out = np.genfromtxt(in_ROM_out_file, delimiter=',')  

        # 7. feedback condition (one-hot encoding with NF as 0)
feedbackCond_csv_file = os.path.normpath(os.path.join(directory, 'feedbackGroups.csv'))
feedbackCond_file = pd.read_csv(feedbackCond_csv_file)
in_cond_SF = np.zeros((36,))
in_cond_TF = np.zeros((36,))
for i in range(1,37):
        if feedbackCond_file.cond[i-1] == 1: # SF
                in_cond_SF[i-1] = 1
        elif feedbackCond_file.cond[i-1] == 2: # TF
                in_cond_TF[i-1] = 1

        # 7b. feedback condition (binary with NF as 0)
in_cond_fb = np.zeros((36,))
for i in range(1,37):
        if feedbackCond_file.cond[i-1] == 1 or feedbackCond_file.cond[i-1] == 2:
                in_cond_fb[i-1] = 1

        # 8. proprio in vs out
in_proprio_in_file = os.path.normpath(os.path.join(directory,'features\\in_proprio_in.csv'))
in_proprio_in = np.abs(np.genfromtxt(in_proprio_in_file, delimiter=','))
in_proprio_in = in_proprio_in[1:]
in_proprio_out_file = os.path.normpath(os.path.join(directory,'features\\in_proprio_out.csv'))
in_proprio_out = np.abs(np.genfromtxt(in_proprio_out_file, delimiter=','))

        # 9. height
in_height_file = os.path.normpath(os.path.join(directory,'features\\in_height.csv'))
in_height = np.abs(np.genfromtxt(in_height_file, delimiter=','))

        # 10. weight
in_weight_file = os.path.normpath(os.path.join(directory,'features\\in_weight.csv'))
in_weight = np.abs(np.genfromtxt(in_weight_file, delimiter=','))

        # 11. sex
in_isFemale_file = os.path.normpath(os.path.join(directory,'features\\in_isFemale.csv'))
in_isFemale = np.abs(np.genfromtxt(in_isFemale_file, delimiter=','))

    # iii. load outputs as numpy arrays:
    # 1. RMSE
out_RMSE_file = os.path.normpath(os.path.join(directory, 'features\\out_RMSE.csv'))
out_RMSE = np.genfromtxt(out_RMSE_file, delimiter=',')
out_RMSE = out_RMSE[1:]

        # 2. delta RMSE
out_delta_RT4 = (out_RMSE[1:,4] - out_RMSE[1:,0])/out_RMSE[1:,0]
out_delta_RET = (out_RMSE[1:,5] - out_RMSE[1:,0])/out_RMSE[1:,0]

        # 3. error ratios
out_errRatio_in_file = os.path.normpath(os.path.join(directory,'features\\out_errRatio_in.csv'))
out_errRatio_in = np.abs(np.genfromtxt(out_errRatio_in_file, delimiter=','))
out_errRatio_out_file = os.path.normpath(os.path.join(directory,'features\\out_errRatio_out.csv'))
out_errRatio_out = np.abs(np.genfromtxt(out_errRatio_out_file, delimiter=','))

        # 4. catch trial RMSE
out_cRMSE_file = os.path.normpath(os.path.join(directory, 'features\\out_cRMSE.csv'))
out_cRMSE = np.genfromtxt(out_cRMSE_file, delimiter=',')

# get cond labels
SF_rows = np.where(feedbackCond_file == 1)[0]
TF_rows = np.where(feedbackCond_file == 2)[0]
FB_rows = np.where((feedbackCond_file == 1) | (feedbackCond_file == 2))[0]
NF_rows = np.where(feedbackCond_file == 0)[0]