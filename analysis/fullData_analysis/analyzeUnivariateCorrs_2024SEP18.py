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

# compute corrs
# ____________________________________bFPA ____________________________________
# plot all
plt.figure(figsize=(10, 6))
plt.subplot(1,2,1)

# get overall reg
slope, intercept, r, p = calc_regression(in_bFPA, out_RMSE[:,4])
line = slope * in_bFPA + intercept

plt.xlabel('bFPA')
plt.ylim([0, 12])
plt.ylabel('RMSE RT4')
plt.plot(in_bFPA, line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')

colors = ['#0f4c5c', '#5f0f40', '#e36414', '#679436']
labels = ['SF', 'TF', 'NF', 'FB']
subgroups = [SF_rows, TF_rows, NF_rows, FB_rows]

for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_bFPA[subgroup], out_RMSE[subgroup,4])
        line_sub = slope_sub * in_bFPA[subgroup] + intercept_sub
        plt.plot(in_bFPA[subgroup], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_bFPA[subgroup], out_RMSE[subgroup,4], alpha=0.5, color = color)
plt.legend()

plt.subplot(1,2,2)

# get overall reg
slope, intercept, r, p = calc_regression(in_bFPA, out_RMSE[:,5])
line = slope * in_bFPA + intercept

plt.xlabel('bFPA')
plt.ylim([0, 12])
plt.ylabel('RMSE RET')
plt.plot(in_bFPA, line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')


for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_bFPA[subgroup], out_RMSE[subgroup,5])
        line_sub = slope_sub * in_bFPA[subgroup] + intercept_sub
        plt.plot(in_bFPA[subgroup], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_bFPA[subgroup], out_RMSE[subgroup,5], alpha=0.5, color = color)
plt.legend()
plt.show()


# ____________________________________responsiveness ____________________________________
# plot all
plt.figure(figsize=(10, 6))
plt.subplot(1,2,1)

# get overall reg
slope, intercept, r, p = calc_regression(in_resp[:,3], out_RMSE[:,4])
line = slope * in_resp[:,3] + intercept

plt.xlabel('responsiveness')
plt.ylim([0, 10])
plt.ylabel('RMSE RT4')
plt.plot(in_resp[:,3], line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')


for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_resp[subgroup,3], out_RMSE[subgroup,4])
        line_sub = slope_sub * in_resp[subgroup,3] + intercept_sub
        plt.plot(in_resp[subgroup,3], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_resp[subgroup,3], out_RMSE[subgroup,3], alpha=0.5, color = color)
plt.legend()

plt.subplot(1,2,2)

# get overall reg
slope, intercept, r, p = calc_regression(in_resp[:,4], out_RMSE[:,5])
line = slope * in_resp[:,4] + intercept

plt.xlabel('responsiveness')
plt.ylim([0, 10])
plt.ylabel('RMSE RET')
plt.plot(in_resp[:,4], line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')

for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_resp[subgroup,4], out_RMSE[subgroup,5])
        line_sub = slope_sub * in_resp[subgroup,4] + intercept_sub
        plt.plot(in_resp[subgroup,4], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_resp[subgroup,4], out_RMSE[subgroup,5], alpha=0.5, color = color)
plt.legend()
plt.show()

# ____________________________________ proprio ____________________________________
# plot all
plt.figure(figsize=(10, 6))
plt.subplot(1,2,1)

# get overall reg
slope, intercept, r, p = calc_regression(in_proprio_in, out_RMSE[:,4])
line = slope * in_proprio_in + intercept

plt.xlabel('proprio error')
#plt.ylim([0, 12])
plt.ylabel('RMSE RT4')
plt.plot(in_proprio_in, line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')


for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_proprio_in[subgroup], out_RMSE[subgroup,4])
        line_sub = slope_sub * in_proprio_in[subgroup] + intercept_sub
        plt.plot(in_proprio_in[subgroup], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_proprio_in[subgroup], out_RMSE[subgroup,4], alpha=0.5, color = color)
plt.legend()

plt.subplot(1,2,2)

# get overall reg
slope, intercept, r, p = calc_regression(in_proprio_in, out_RMSE[:,5])
line = slope * in_proprio_in + intercept

plt.xlabel('proprio error')
#plt.ylim([0, 12])
plt.ylabel('RMSE RET')
plt.plot(in_proprio_in, line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')

for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_proprio_in[subgroup], out_RMSE[subgroup,5])
        line_sub = slope_sub * in_proprio_in[subgroup] + intercept_sub
        plt.plot(in_proprio_in[subgroup], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_proprio_in[subgroup], out_RMSE[subgroup,5], alpha=0.5, color = color)
plt.legend()
plt.show()


# ____________________________________ ROM ____________________________________
# plot all
plt.figure(figsize=(10, 6))
plt.subplot(1,2,1)

# get overall reg
slope, intercept, r, p = calc_regression(in_ROM_in, out_RMSE[:,4])
line = slope * in_ROM_in + intercept

plt.xlabel('ROM')
#plt.ylim([0, 12])
plt.ylabel('RMSE RT4')
plt.plot(in_ROM_in, line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')


for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_ROM_in[subgroup], out_RMSE[subgroup,4])
        line_sub = slope_sub * in_ROM_in[subgroup] + intercept_sub
        plt.plot(in_ROM_in[subgroup], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_ROM_in[subgroup], out_RMSE[subgroup,4], alpha=0.5, color = color)
plt.legend()

plt.subplot(1,2,2)

# get overall reg
slope, intercept, r, p = calc_regression(in_ROM_in, out_RMSE[:,5])
line = slope * in_ROM_in + intercept

plt.xlabel('ROM')
#plt.ylim([0, 12])
plt.ylabel('RMSE RET')
plt.plot(in_ROM_in, line, color='black', label=f'Overall (R={r:.2f}, p={p:.3f})')

for i, (subgroup, color, label) in enumerate(zip(subgroups, colors, labels)):
    if len(subgroup) > 0:
        slope_sub, intercept_sub, r_sub, p_sub = calc_regression(in_ROM_in[subgroup], out_RMSE[subgroup,5])
        line_sub = slope_sub * in_ROM_in[subgroup] + intercept_sub
        plt.plot(in_ROM_in[subgroup], line_sub, color=color, alpha = 0.5, label=f'{label} (R={r_sub:.2f}, p={p_sub:.3f})')
        plt.scatter(in_ROM_in[subgroup], out_RMSE[subgroup,5], alpha=0.5, color = color)
plt.legend()
plt.show()