import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog

# 1. LOAD FPA DATA
# a. Get the desired directory to save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

subs_tot = 21
store_inRangePercent = np.zeros((subs_tot, 6)) #toein1-4, ret
store_inRangeNFPercent = np.zeros((subs_tot, 6)) #toein1-4, ret
store_meanFPASD = np.zeros((subs_tot, 6, 2)) #toein1-4, ret

vis = 0


# b. load subject data
for subject in range(1,34):
    if subject > 20 and subject < 34:
        continue

    print('----------------Starting analysis for subject ' + str(subject) + '--------------------')

    if subject < 10:
        baseline_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_baseline_meanFPA.csv'))
        baselineFPA = pd.read_csv(baseline_csv_file)

        # apparently dynamic variable naming is bad practice 
        nf_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_noFB_meanFPA.csv'))
        nfFPA = pd.read_csv(nf_csv_file)

        toein1_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA_1.csv'))
        toein1FPA = pd.read_csv(toein1_csv_file)

        toein2_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA_2.csv'))
        toein2FPA = pd.read_csv(toein2_csv_file)

        toein3_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA_3.csv'))
        toein3FPA = pd.read_csv(toein3_csv_file)

        toein4_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_meanFPA_4.csv'))
        toein4FPA = pd.read_csv(toein4_csv_file)

        ret_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_retention_meanFPA.csv'))
        retFPA = pd.read_csv(ret_csv_file)

        fullFPA = pd.concat([baselineFPA, toein1FPA, toein2FPA, toein3FPA, toein4FPA, retFPA])
    else:
        baseline_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_baseline_meanFPA.csv'))
        baselineFPA = pd.read_csv(baseline_csv_file)

        # apparently dynamic variable naming is bad practice 
        nf_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_noFB_meanFPA.csv'))
        nfFPA = pd.read_csv(nf_csv_file)

        toein1_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_meanFPA_1.csv'))
        toein1FPA = pd.read_csv(toein1_csv_file)

        toein2_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_meanFPA_2.csv'))
        toein2FPA = pd.read_csv(toein2_csv_file)

        toein3_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_meanFPA_3.csv'))
        toein3FPA = pd.read_csv(toein3_csv_file)

        toein4_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_meanFPA_4.csv'))
        toein4FPA = pd.read_csv(toein4_csv_file)

        ret_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_retention_meanFPA.csv'))
        retFPA = pd.read_csv(ret_csv_file)

        fullFPA = pd.concat([baselineFPA, toein1FPA, toein2FPA, toein3FPA, toein4FPA, retFPA])


    # c. extract baseline FPA
    bFPA_deg = np.mean(baselineFPA.iloc[:,2])
    print('Baseline FPA was: ' + str(bFPA_deg) + '(' + str(np.std(baselineFPA.iloc[:,2])) + ')')

    # TODO: use an index for the catch trials to make .iloc easier
    catch1 = len(baselineFPA) + len(toein1FPA)/2
    catch2 = len(baselineFPA) + len(toein1FPA) + len(toein2FPA)/2
    catch3 = len(baselineFPA) + len(toein1FPA) + len(toein2FPA) + len(toein3FPA)/2
    catch4 = len(baselineFPA) + len(toein1FPA) + len(toein2FPA) + len(toein3FPA) + len(toein4FPA)/2

    print('TI1: ' + str(np.mean(toein1FPA.iloc[:,2])) + '(' + str(np.std(toein1FPA.iloc[:,2])) + ')')
    print('C1: ' + str(np.mean(fullFPA.iloc[int(catch1):int(catch1+40),2])) + '(' + str(np.std(fullFPA.iloc[int(catch1):int(catch1+40),2])) + ')')
    print('TI2: ' + str(np.mean(toein2FPA.iloc[:,2])) + '(' + str(np.std(toein2FPA.iloc[:,2])) + ')')
    print('C2: ' + str(np.mean(fullFPA.iloc[int(catch2):int(catch2+40),2])) + '(' + str(np.std(fullFPA.iloc[int(catch2):int(catch2+40),2])) + ')')
    print('TI3: ' + str(np.mean(toein3FPA.iloc[:,2])) + '(' + str(np.std(toein3FPA.iloc[:,2])) + ')')
    print('C3: ' + str(np.mean(fullFPA.iloc[int(catch3):int(catch3+40),2])) + '(' + str(np.std(fullFPA.iloc[int(catch3):int(catch3+40),2])) + ')')
    print('TI4: ' + str(np.mean(toein4FPA.iloc[:,2])) + '(' + str(np.std(toein4FPA.iloc[:,2])) + ')')
    print('C4: ' + str(np.mean(fullFPA.iloc[int(catch4):int(catch4+40),2])) + '(' + str(np.std(fullFPA.iloc[int(catch4):int(catch4+40),2])) + ')')
    print('Re: ' + str(np.mean(retFPA.iloc[:,2])) + '(' + str(np.std(retFPA.iloc[:,2])) + ')')

    if vis:
        # d. generate plot of all FPA across time
        x = np.linspace(0, len(fullFPA), len(fullFPA))
        plt.plot(x, fullFPA.iloc[:,2], '--o')

        # vertical lines for retraining periods: 
        plt.vlines(x = len(baselineFPA)+1, ymin = -25.0, ymax = 15.0, colors = 'k') # toein 1 start time
        plt.vlines(x = len(baselineFPA)+len(toein1FPA)+1, ymin = -25.0, ymax = 15.0, colors = 'k') # toein 2 start time
        plt.vlines(x = len(baselineFPA)+len(toein1FPA)+len(toein2FPA)+1, ymin = -25.0, ymax = 15.0, colors = 'k') # toein 3 start time
        plt.vlines(x = len(baselineFPA)+len(toein1FPA)+len(toein2FPA)+len(toein3FPA)+1, ymin = -25.0, ymax = 15.0, colors = 'k') # toein 4 start time
        plt.vlines(x = len(fullFPA) - len(retFPA)+1, ymin = -25.0, ymax = 15.0, colors = 'k') # retention start time

        # vertical lines for catch trials:
        plt.vlines(x = catch1, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 1 start time
        plt.vlines(x = catch1 + 40, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 1 end time

        plt.vlines(x = catch2, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 2 start time
        plt.vlines(x = catch2 + 40, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 2 end time

        plt.vlines(x = catch3, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 3 start time
        plt.vlines(x = catch3 + 40, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 3 end time

        plt.vlines(x = catch4, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 4 start time
        plt.vlines(x = catch4 + 40, ymin = -25.0, ymax = 15.0, colors = 'k', linestyles = '--') # catch 4 end time 
        # horizontal line for target FPA:
        plt.hlines(y = bFPA_deg-10, xmin = len(baselineFPA)+1, xmax = len(fullFPA), colors = 'r', linestyles = '--')

        plt.ylim([-25,15]) #TODO: set this to be consistent across all subs based on all-sub max and min FPAs (approx.)
        plt.xlabel('Step number')
        plt.ylabel('FPA (deg)')
        plt.title('Walking trials FPA: S0' + str(subject))
        plt.show()

        # new fig: plot running mean
        x = np.linspace(0, len(fullFPA), len(fullFPA))
        plt.plot(x, fullFPA.iloc[:,2], 'o', alpha = 0.5, )
        window_size = 20
        kernel = np.ones(window_size)/window_size
        runnavg = np.convolve(fullFPA.iloc[:,2], kernel, mode = 'same')
        plt.plot(x, runnavg, '-')
        plt.show()
    
            
    # save metrics to subject folder to analyze in aggregate:

    # a. get % of steps in-range: 5 conds x 1 
    targetFPA = bFPA_deg-10
    inRange_nf = 100*len(nfFPA[(nfFPA.iloc[:,2]<targetFPA+2) & (nfFPA.iloc[:,2]>targetFPA-2)])/len(nfFPA)
    print('percent steps in range during NF: ' + str(inRange_nf))
    inRange_t1 = 100*len(toein1FPA[(toein1FPA.iloc[:,2]<targetFPA+2) & (toein1FPA.iloc[:,2]>targetFPA-2)])/len(toein1FPA)
    print('percent steps in range during toe-in 1: ' + str(inRange_t1)) 
    inRange_t2 = 100*len(toein2FPA[(toein2FPA.iloc[:,2]<targetFPA+2) & (toein2FPA.iloc[:,2]>targetFPA-2)])/len(toein2FPA)
    print('percent steps in range during toe-in 2: ' + str(inRange_t2)) 
    inRange_t3 = 100*len(toein3FPA[(toein3FPA.iloc[:,2]<targetFPA+2) & (toein3FPA.iloc[:,2]>targetFPA-2)])/len(toein3FPA)
    print('percent steps in range during toe-in 3: ' + str(inRange_t3)) 
    inRange_t4 = 100*len(toein4FPA[(toein4FPA.iloc[:,2]<targetFPA+2) & (toein4FPA.iloc[:,2]>targetFPA-2)])/len(toein4FPA)
    print('percent steps in range during toe-in 4: ' + str(inRange_t4)) 
    inRange_ret = 100*len(retFPA[(retFPA.iloc[:,2]<targetFPA+2) & (retFPA.iloc[:,2]>targetFPA-2)])/len(retFPA)
    print('percent steps in range during retention: ' + str(inRange_ret)) 

    # get % of steps in-range in catch trials:
    inRange_c1 = 100 * len(toein1FPA.iloc[80:121][(toein1FPA.iloc[80:121, 2] < targetFPA + 2) & (toein1FPA.iloc[80:121, 2] > targetFPA - 2)]) / 40
    print('percent steps in range during catch 1: ' + str(inRange_c1)) 
    inRange_c2 = 100 * len(toein2FPA.iloc[80:121][(toein2FPA.iloc[80:121, 2] < targetFPA + 2) & (toein2FPA.iloc[80:121, 2] > targetFPA - 2)]) / 40
    print('percent steps in range during catch 2: ' + str(inRange_c2))
    inRange_c3 = 100 * len(toein3FPA.iloc[80:121][(toein3FPA.iloc[80:121, 2] < targetFPA + 2) & (toein3FPA.iloc[80:121, 2] > targetFPA - 2)]) / 40
    print('percent steps in range during catch 3: ' + str(inRange_c3))
    inRange_c4 = 100 * len(toein4FPA.iloc[80:121][(toein4FPA.iloc[80:121, 2] < targetFPA + 2) & (toein4FPA.iloc[80:121, 2] > targetFPA - 2)]) / 40
    print('percent steps in range during catch 4: ' + str(inRange_c4))
     

    inRange_all = [inRange_nf, inRange_t1, inRange_t2, inRange_t3, inRange_t4, inRange_ret]
    inRange_NFs = [inRange_nf, inRange_c1, inRange_c2, inRange_c3, inRange_c4, inRange_ret]
    store_inRangePercent[subject-1] = inRange_all
    store_inRangeNFPercent[subject-1] = inRange_NFs

    # b. get relative mean(SD) FPA per block
    meanNF = bFPA_deg - np.mean(nfFPA.iloc[:,2])
    stdNF = np.std(nfFPA.iloc[:,2])
    meanT1 = bFPA_deg - np.mean(toein1FPA.iloc[:,2])
    stdT1 = np.std(toein1FPA.iloc[:,2])
    meanT2 = bFPA_deg - np.mean(toein2FPA.iloc[:,2])
    stdT2 = np.std(toein2FPA.iloc[:,2])
    meanT3 = bFPA_deg - np.mean(toein3FPA.iloc[:,2])
    stdT3 = np.std(toein3FPA.iloc[:,2])
    meanT4 = bFPA_deg - np.mean(toein4FPA.iloc[:,2])
    stdT4 = np.std(toein4FPA.iloc[:,2])
    meanR = bFPA_deg - np.mean(retFPA.iloc[:,2])
    stdR = np.std(retFPA.iloc[:,2])

    pairedMeanSTD = [(meanNF, stdNF), (meanT1, stdT1), (meanT2, stdT2), (meanT3, stdT3), (meanT4, stdT4), (meanR, stdR)]
    store_meanFPASD[subject-1] = pairedMeanSTD

# plot group means for cumulative results: percent steps in range
SF_rows = [0, 1, 6, 8, 11, 14, 18]
TF_rows = [2, 3, 7, 12, 15, 19, 20]
NF_rows = [4, 5, 9, 10, 13, 16, 17]
x = np.arange(6)

plt.plot(x, np.mean(store_inRangePercent[SF_rows], axis=0), '-o', color = '#05668D', label = 'SF')
plt.errorbar(x, np.mean(store_inRangePercent[SF_rows], axis=0), yerr=np.std(store_inRangePercent[SF_rows], axis=0), fmt='none', ecolor='#05668D', capsize=5)

plt.plot(x, np.mean(store_inRangePercent[TF_rows], axis=0), '-o', color = '#679436', label = 'TF')
plt.errorbar(x, np.mean(store_inRangePercent[TF_rows], axis=0), yerr=np.std(store_inRangePercent[TF_rows], axis=0), fmt='none', ecolor='#679436', capsize=5)

plt.plot(x, np.mean(store_inRangePercent[NF_rows], axis=0), '-o', color = '#805E73', label = 'NF')
plt.errorbar(x, np.mean(store_inRangePercent[NF_rows], axis=0), yerr=np.std(store_inRangePercent[NF_rows], axis=0), fmt='none', ecolor='#805E73', capsize=5)

plt.legend()
plt.ylim([0,100])
plt.ylabel('Steps within target range (%)')
plt.show()

# plot group means for cumulative results: percent steps in range during NF conds
plt.plot(x, np.mean(store_inRangeNFPercent[SF_rows], axis=0), '-o', color = '#05668D', label = 'SF')
plt.errorbar(x, np.mean(store_inRangeNFPercent[SF_rows], axis=0), yerr=np.std(store_inRangeNFPercent[SF_rows], axis=0), fmt='none', ecolor='#05668D', capsize=5)

plt.plot(x, np.mean(store_inRangeNFPercent[TF_rows], axis=0), '-o', color = '#679436', label = 'TF')
plt.errorbar(x, np.mean(store_inRangeNFPercent[TF_rows], axis=0), yerr=np.std(store_inRangeNFPercent[TF_rows], axis=0), fmt='none', ecolor='#679436', capsize=5)

plt.plot(x, np.mean(store_inRangeNFPercent[NF_rows], axis=0), '-o', color = '#805E73', label = 'NF')
plt.errorbar(x, np.mean(store_inRangeNFPercent[NF_rows], axis=0), yerr=np.std(store_inRangeNFPercent[NF_rows], axis=0), fmt='none', ecolor='#805E73', capsize=5)

plt.legend()
plt.ylim([0,100])
plt.ylabel('Steps within target range (%)')
plt.show()

# plot group means for cumulative results: mean abs error in FPA
plt.plot(x, np.abs(10-np.mean(store_meanFPASD[SF_rows, :, 0], axis=0)), '-o', color = '#05668D', label = 'SF')
plt.errorbar(x, np.abs(10-np.mean(store_meanFPASD[SF_rows, :, 0], axis=0)), yerr=np.std(store_meanFPASD[SF_rows, :, 0], axis=0), fmt='none', ecolor='#05668D', capsize=5)
plt.plot(x, np.abs(10-np.mean(store_meanFPASD[TF_rows, :, 0], axis=0)), '-o', color = '#679436', label = 'TF')
plt.errorbar(x, np.abs(10-np.mean(store_meanFPASD[TF_rows, :, 0], axis=0)), yerr=np.std(store_meanFPASD[TF_rows, :, 0], axis=0), fmt='none', ecolor='#05668D', capsize=5)
plt.plot(x, np.abs(10-np.mean(store_meanFPASD[NF_rows, :, 0], axis=0)), '-o', color = '#805E73', label = 'NF')
plt.errorbar(x, np.abs(10-np.mean(store_meanFPASD[NF_rows, :, 0], axis=0)), yerr=np.std(store_meanFPASD[NF_rows, :, 0], axis=0), fmt='none', ecolor='#05668D', capsize=5)
# todo: change the way i'm storing mean(SD) error 


plt.legend()
plt.ylabel('Mean FPA error (deg)')
plt.show()