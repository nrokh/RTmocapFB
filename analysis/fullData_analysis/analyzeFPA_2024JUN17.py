import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from scipy import stats
from matplotlib.colors import to_rgba
import ptitprince as pt 
import seaborn as sns


# 1. LOAD FPA DATA
# a. Get the desired directory to save the data
root = tk.Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
directory = filedialog.askdirectory()

subs_tot = 36
store_inRangePercent = np.zeros((subs_tot, 6)) #toein1-4, ret
store_inRangeNFPercent = np.zeros((subs_tot, 6)) #toein1-4, ret
store_meanFPASD = np.zeros((subs_tot, 6, 2)) #toein1-4, ret
store_MAE = np.zeros((subs_tot, 6))
store_allFPA_NF = np.zeros((subs_tot, 80))
store_allFPA_RT4 = np.zeros((subs_tot, 200))
store_allFPA_RET = np.zeros((subs_tot, 200))
store_RMSE = np.zeros((subs_tot, 6))
store_resp = np.zeros((subs_tot, 6))
store_proprio_RMSE = np.zeros((subs_tot,1))
store_proprio_MSE_in = np.zeros((subs_tot,1))
store_proprio_MSE_out = np.zeros((subs_tot,1))
store_vbtest_acc = np.zeros((subs_tot,1))
store_ROM_in = np.zeros((subs_tot,1))
store_ROM_out = np.zeros((subs_tot,1))
store_bFPA = np.zeros((subs_tot,1))
store_errorRatio_in = np.zeros((subs_tot, 6))
store_errorRatio_out = np.zeros((subs_tot, 6))

# load feedback condition ID (1:SF, 2:TF, 0:NF)
feedbackCond_csv_file = os.path.normpath(os.path.join(directory, 'feedbackGroups.csv'))
feedbackCond_file = pd.read_csv(feedbackCond_csv_file)

# load setPairings for vbtest
vbtestPairings_csv_file = os.path.normpath(os.path.join(directory, 'setPairingsVBTest.csv'))
vbtestPairings_file = pd.read_csv(vbtestPairings_csv_file)

vis = 0
rmCatchSteps = 1
rmInRange = 0
zeroInRange = 1

# supporting functions
def calculate_responsiveness(input_FPA, targetFPA):
    incorrect_steps = 0
    resp_tally = 0
    
    for step in range(len(input_FPA) - 1):
        current_fpa = input_FPA.iloc[step, 2]
        next_fpa = input_FPA.iloc[step + 1, 2]
        
        if current_fpa < targetFPA - 2:
            incorrect_steps += 1
            if next_fpa > current_fpa:
                resp_tally += 1
        
        elif current_fpa > targetFPA + 2:
            incorrect_steps += 1
            if next_fpa < current_fpa:
                resp_tally += 1
    
    store_resp = resp_tally / incorrect_steps if incorrect_steps > 0 else 0
    
    return store_resp

# 2. load subject data
for subject in range(1,37):

    print('----------------Starting analysis for subject ' + str(subject) + '--------------------')
    if feedbackCond_file.cond[subject-1] == 1:
        print('----------------CONDITION: SCALED FEEDBACK------------')
    elif feedbackCond_file.cond[subject-1] == 2:
        print('----------------CONDITION: TRINARY FEEDBACK------------')
    elif feedbackCond_file.cond[subject-1] == 0:
        print('----------------CONDITION: NO FEEDBACK------------')
    else:
        print('!!!--------ERROR: check feedback condition file?---------!!!')

    if subject < 10:
        # load proprio:
        proprio_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_proprioception.csv'))
        proprio = pd.read_csv(proprio_csv_file)

        # load vbtest: 
        vbtest_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_day1_vbtest.csv'))
        vbtest = np.genfromtxt(vbtest_csv_file, delimiter=',')

        # load ROM:
        ROM_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_ROM_meanFPA.csv'))
        ROM = pd.read_csv(ROM_csv_file)

        # load FPAs:
        baseline_csv_file = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\s0' + str(subject) + '_baseline_meanFPA.csv'))
        baselineFPA = pd.read_csv(baseline_csv_file)

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
        # load proprio:
        proprio_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_proprioception.csv'))
        proprio = pd.read_csv(proprio_csv_file)

        # load vbtest: 
        vbtest_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_day1_vbtest.csv'))
        vbtest = np.genfromtxt(vbtest_csv_file, delimiter=',')

        # load ROM:
        ROM_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_ROM_meanFPA.csv'))
        ROM = pd.read_csv(ROM_csv_file)

        baseline_csv_file = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\s' + str(subject) + '_baseline_meanFPA.csv'))
        baselineFPA = pd.read_csv(baseline_csv_file)

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

    store_bFPA[subject-1] = bFPA_deg


    if vis:
        # fig: plot running mean
        x = np.linspace(0, len(fullFPA), len(fullFPA))
        plt.plot(x, fullFPA.iloc[:,2], 'o', alpha = 0.5, )
        window_size = 20
        kernel = np.ones(window_size)/window_size
        runnavg = np.convolve(fullFPA.iloc[:,2], kernel, mode = 'same')
        plt.plot(x, runnavg, '-')
        plt.show()

    # a. get % of steps in-range: 5 conds x 1 
    targetFPA = bFPA_deg-10

    inRange_nf = 100*len(nfFPA[(nfFPA.iloc[:,2]<targetFPA+2) & (nfFPA.iloc[:,2]>targetFPA-2)])/len(nfFPA)
    print('percent steps in range during NF: ' + str(inRange_nf))

    if rmCatchSteps:

        inRange_t1 = 100 * len(pd.concat([toein1FPA.iloc[:80], toein1FPA.iloc[121:]])[(pd.concat([toein1FPA.iloc[:80], toein1FPA.iloc[121:]]).iloc[:, 2] < targetFPA + 2) & (pd.concat([toein1FPA.iloc[:80], toein1FPA.iloc[121:]]).iloc[:, 2] > targetFPA - 2)]) / (len(toein1FPA) - 41)
        print('percent steps in range during toe-in 1: ' + str(inRange_t1))
        inRange_t2 = 100 * len(pd.concat([toein2FPA.iloc[:80], toein2FPA.iloc[121:]])[(pd.concat([toein2FPA.iloc[:80], toein2FPA.iloc[121:]]).iloc[:, 2] < targetFPA + 2) & (pd.concat([toein2FPA.iloc[:80], toein2FPA.iloc[121:]]).iloc[:, 2] > targetFPA - 2)]) / (len(toein2FPA) - 41)
        print('percent steps in range during toe-in 2: ' + str(inRange_t2))
        inRange_t3 = 100 * len(pd.concat([toein3FPA.iloc[:80], toein3FPA.iloc[121:]])[(pd.concat([toein3FPA.iloc[:80], toein3FPA.iloc[121:]]).iloc[:, 2] < targetFPA + 2) & (pd.concat([toein3FPA.iloc[:80], toein3FPA.iloc[121:]]).iloc[:, 2] > targetFPA - 2)]) / (len(toein3FPA) - 41)
        print('percent steps in range during toe-in 3: ' + str(inRange_t3))
        inRange_t4 = 100 * len(pd.concat([toein4FPA.iloc[:80], toein4FPA.iloc[121:]])[(pd.concat([toein4FPA.iloc[:80], toein4FPA.iloc[121:]]).iloc[:, 2] < targetFPA + 2) & (pd.concat([toein4FPA.iloc[:80], toein4FPA.iloc[121:]]).iloc[:, 2] > targetFPA - 2)]) / (len(toein4FPA) - 41)
        print('percent steps in range during toe-in 4: ' + str(inRange_t4))

    else:
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

    # b.ii: store all tFPA:
    if subject==11:
        allFPA_RT4 = bFPA_deg - toein3FPA.iloc[:,2]
    else:
        allFPA_RT4 = bFPA_deg - toein4FPA.iloc[:,2]
    allFPA_NF = bFPA_deg - nfFPA.iloc[:,2]
    allFPA_RET = bFPA_deg - retFPA.iloc[:,2]

    store_allFPA_NF[subject-1] =  allFPA_NF
    store_allFPA_RT4[subject-1] = allFPA_RT4
    store_allFPA_RET[subject-1] = allFPA_RET

    # save tFPAs:
    if subject < 10:
        store_allFPA_NF = pd.DataFrame(allFPA_NF)
        output_NF = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_NF.csv'))
        store_allFPA_NF.to_csv(output_NF, index=False)

        store_allFPA_RT4 = pd.DataFrame(allFPA_RT4)
        output_RT4 = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_RT4.csv'))
        store_allFPA_RT4.to_csv(output_RT4, index=False)

        store_allFPA_RET = pd.DataFrame(allFPA_RET)
        output_RET = os.path.normpath(os.path.join(directory, 's0' + str(subject)  + '\\tFPA_RET.csv'))
        store_allFPA_RET.to_csv(output_RET, index=False)
    else:
        store_allFPA_NF = pd.DataFrame(allFPA_NF)
        output_NF = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_NF.csv'))
        store_allFPA_NF.to_csv(output_NF, index=False)

        store_allFPA_RT4 = pd.DataFrame(allFPA_RT4)
        output_RT4 = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_RT4.csv'))
        store_allFPA_RT4.to_csv(output_RT4, index=False)

        store_allFPA_RET = pd.DataFrame(allFPA_RET)
        output_RET = os.path.normpath(os.path.join(directory, 's' + str(subject)  + '\\tFPA_RET.csv'))
        store_allFPA_RET.to_csv(output_RET, index=False)
        

    # c. get MAE for FPA:
    if rmInRange:
        MAENF = np.mean(np.abs(bFPA_deg - 10 - nfFPA.iloc[:,2])[(nfFPA.iloc[:,2] > targetFPA + 2) | (nfFPA.iloc[:,2] < targetFPA - 2)])
        MAET1 = np.mean(np.abs(bFPA_deg - 10 - toein1FPA.iloc[:,2])[(toein1FPA.iloc[:,2] > targetFPA + 2) | (toein1FPA.iloc[:,2] < targetFPA - 2)])
        MAET2 = np.mean(np.abs(bFPA_deg - 10 - toein2FPA.iloc[:,2])[(toein2FPA.iloc[:,2] > targetFPA + 2) | (toein2FPA.iloc[:,2] < targetFPA - 2)])
        MAET3 = np.mean(np.abs(bFPA_deg - 10 - toein3FPA.iloc[:,2])[(toein3FPA.iloc[:,2] > targetFPA + 2) | (toein3FPA.iloc[:,2] < targetFPA - 2)])
        MAET4 = np.mean(np.abs(bFPA_deg - 10 - toein4FPA.iloc[:,2])[(toein4FPA.iloc[:,2] > targetFPA + 2) | (toein4FPA.iloc[:,2] < targetFPA - 2)])
        MAER = np.mean(np.abs(bFPA_deg - 10 - retFPA.iloc[:,2])[(retFPA.iloc[:,2] > targetFPA + 2) | (retFPA.iloc[:,2] < targetFPA - 2)])
               
    elif zeroInRange:
        adjusted_nfFPA = np.where((nfFPA.iloc[:,2] >= targetFPA - 2) & (nfFPA.iloc[:,2] <= targetFPA + 2), targetFPA, nfFPA.iloc[:,2])
        adjusted_toein1FPA = np.where((toein1FPA.iloc[:,2] >= targetFPA - 2) & (toein1FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein1FPA.iloc[:,2])
        adjusted_toein2FPA = np.where((toein2FPA.iloc[:,2] >= targetFPA - 2) & (toein2FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein2FPA.iloc[:,2])
        adjusted_toein3FPA = np.where((toein3FPA.iloc[:,2] >= targetFPA - 2) & (toein3FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein3FPA.iloc[:,2])
        adjusted_toein4FPA = np.where((toein4FPA.iloc[:,2] >= targetFPA - 2) & (toein4FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein4FPA.iloc[:,2])
        adjusted_retFPA = np.where((retFPA.iloc[:,2] >= targetFPA - 2) & (retFPA.iloc[:,2] <= targetFPA + 2), targetFPA, retFPA.iloc[:,2])
        MAENF = np.mean(np.abs(bFPA_deg - 10 - adjusted_nfFPA))
        MAET1 = np.mean(np.abs(bFPA_deg - 10 - adjusted_toein1FPA))
        MAET2 = np.mean(np.abs(bFPA_deg - 10 - adjusted_toein2FPA))
        MAET3 = np.mean(np.abs(bFPA_deg - 10 - adjusted_toein3FPA))
        MAET4 = np.mean(np.abs(bFPA_deg - 10 - adjusted_toein4FPA))
        MAER = np.mean(np.abs(bFPA_deg - 10 - adjusted_retFPA))

    else:
        MAENF = np.mean(np.abs(bFPA_deg - 10 - nfFPA.iloc[:,2]))
        MAET1 = np.mean(np.abs(bFPA_deg - 10 - toein1FPA.iloc[:,2]))
        MAET2 = np.mean(np.abs(bFPA_deg - 10 - toein2FPA.iloc[:,2]))
        MAET3 = np.mean(np.abs(bFPA_deg - 10 - toein3FPA.iloc[:,2]))
        MAET4 = np.mean(np.abs(bFPA_deg - 10 - toein4FPA.iloc[:,2]))
        MAER = np.mean(np.abs(bFPA_deg - 10 - retFPA.iloc[:,2]))

    MAE_all = [MAENF, MAET1, MAET2, MAET3, MAET4, MAER]
    store_MAE[subject-1] = MAE_all

    # d. get RMSE for FPA:
    if rmInRange:
        RMSENF = np.sqrt(np.mean(((bFPA_deg - 10 - nfFPA.iloc[:,2])[(nfFPA.iloc[:,2] > targetFPA + 2) | (nfFPA.iloc[:,2] < targetFPA - 2)])**2))
        RMSET1 = np.sqrt(np.mean(((bFPA_deg - 10 - toein1FPA.iloc[:,2])[(toein1FPA.iloc[:,2] > targetFPA + 2) | (toein1FPA.iloc[:,2] < targetFPA - 2)])**2))
        RMSET2 = np.sqrt(np.mean(((bFPA_deg - 10 - toein2FPA.iloc[:,2])[(toein2FPA.iloc[:,2] > targetFPA + 2) | (toein2FPA.iloc[:,2] < targetFPA - 2)])**2))
        RMSET3 = np.sqrt(np.mean(((bFPA_deg - 10 - toein3FPA.iloc[:,2])[(toein3FPA.iloc[:,2] > targetFPA + 2) | (toein3FPA.iloc[:,2] < targetFPA - 2)])**2))
        RMSET4 = np.sqrt(np.mean(((bFPA_deg - 10 - toein4FPA.iloc[:,2])[(toein4FPA.iloc[:,2] > targetFPA + 2) | (toein4FPA.iloc[:,2] < targetFPA - 2)])**2))
        RMSER = np.sqrt(np.mean(((bFPA_deg - 10 - retFPA.iloc[:,2])[(retFPA.iloc[:,2] > targetFPA + 2) | (retFPA.iloc[:,2] < targetFPA - 2)])**2))
  
    elif zeroInRange:
        adjusted_nfFPA = np.where((nfFPA.iloc[:,2] >= targetFPA - 2) & (nfFPA.iloc[:,2] <= targetFPA + 2), targetFPA, nfFPA.iloc[:,2])
        adjusted_toein1FPA = np.where((toein1FPA.iloc[:,2] >= targetFPA - 2) & (toein1FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein1FPA.iloc[:,2])
        adjusted_toein2FPA = np.where((toein2FPA.iloc[:,2] >= targetFPA - 2) & (toein2FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein2FPA.iloc[:,2])
        adjusted_toein3FPA = np.where((toein3FPA.iloc[:,2] >= targetFPA - 2) & (toein3FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein3FPA.iloc[:,2])
        adjusted_toein4FPA = np.where((toein4FPA.iloc[:,2] >= targetFPA - 2) & (toein4FPA.iloc[:,2] <= targetFPA + 2), targetFPA, toein4FPA.iloc[:,2])
        adjusted_retFPA = np.where((retFPA.iloc[:,2] >= targetFPA - 2) & (retFPA.iloc[:,2] <= targetFPA + 2), targetFPA, retFPA.iloc[:,2])
        RMSENF = np.sqrt(np.mean( (bFPA_deg-10-adjusted_nfFPA)**2 ))
        RMSET1 = np.sqrt(np.mean( (bFPA_deg-10-adjusted_toein1FPA)**2 ))
        RMSET2 = np.sqrt(np.mean( (bFPA_deg-10-adjusted_toein2FPA)**2 ))
        RMSET3 = np.sqrt(np.mean( (bFPA_deg-10-adjusted_toein3FPA)**2 ))
        RMSET4 = np.sqrt(np.mean( (bFPA_deg-10-adjusted_toein4FPA)**2 ))
        RMSER = np.sqrt(np.mean( (bFPA_deg-10-adjusted_retFPA)**2 ))
    else:
        RMSENF = np.sqrt(np.mean( (bFPA_deg-10-nfFPA.iloc[:,2])**2 ))
        RMSET1 = np.sqrt(np.mean( (bFPA_deg-10-toein1FPA.iloc[:,2])**2 ))
        RMSET2 = np.sqrt(np.mean( (bFPA_deg-10-toein2FPA.iloc[:,2])**2 ))
        RMSET3 = np.sqrt(np.mean( (bFPA_deg-10-toein3FPA.iloc[:,2])**2 ))
        RMSET4 = np.sqrt(np.mean( (bFPA_deg-10-toein4FPA.iloc[:,2])**2 ))
        RMSER = np.sqrt(np.mean( (bFPA_deg-10-retFPA.iloc[:,2])**2 ))

    RMSE_all = [RMSENF, RMSET1, RMSET2, RMSET3, RMSET4, RMSER]
    store_RMSE[subject-1] = RMSE_all

    # d.2. get ratio of steps too far in vs. too far out
    errorRatio_NF_in = np.sum(nfFPA.iloc[:, 2] <= targetFPA - 2)/len(nfFPA.iloc[:, 2])
    errorRatio_RT1_in = np.sum(toein1FPA.iloc[:, 2] <= targetFPA - 2)/len(toein1FPA.iloc[:, 2])
    errorRatio_RT2_in = np.sum(toein2FPA.iloc[:, 2] <= targetFPA - 2)/len(toein2FPA.iloc[:, 2])
    errorRatio_RT3_in = np.sum(toein3FPA.iloc[:, 2] <= targetFPA - 2)/len(toein3FPA.iloc[:, 2])
    errorRatio_RT4_in = np.sum(toein4FPA.iloc[:, 2] <= targetFPA - 2)/len(toein4FPA.iloc[:, 2])
    errorRatio_RET_in = np.sum(retFPA.iloc[:, 2] <= targetFPA - 2)/len(retFPA.iloc[:, 2])

    errorRatio_in_all = [errorRatio_NF_in, errorRatio_RT1_in, errorRatio_RT2_in, errorRatio_RT3_in, errorRatio_RT4_in, errorRatio_RET_in]
    store_errorRatio_in[subject-1] = errorRatio_in_all

    errorRatio_NF_out = np.sum(nfFPA.iloc[:, 2] >= targetFPA + 2)/len(nfFPA.iloc[:, 2])
    errorRatio_RT1_out = np.sum(toein1FPA.iloc[:, 2] >= targetFPA + 2)/len(toein1FPA.iloc[:, 2])
    errorRatio_RT2_out = np.sum(toein2FPA.iloc[:, 2] >= targetFPA + 2)/len(toein2FPA.iloc[:, 2])
    errorRatio_RT3_out = np.sum(toein3FPA.iloc[:, 2] >= targetFPA + 2)/len(toein3FPA.iloc[:, 2])
    errorRatio_RT4_out = np.sum(toein4FPA.iloc[:, 2] >= targetFPA + 2)/len(toein4FPA.iloc[:, 2])
    errorRatio_RET_out = np.sum(retFPA.iloc[:, 2] >= targetFPA + 2)/len(retFPA.iloc[:, 2])

    errorRatio_out_all = [errorRatio_NF_out, errorRatio_RT1_out, errorRatio_RT2_out, errorRatio_RT3_out, errorRatio_RT4_out, errorRatio_RET_out]
    store_errorRatio_out[subject-1] = errorRatio_out_all


    # e. get responsiveness
    store_resp_NF = calculate_responsiveness(nfFPA, targetFPA)
    store_resp_RT1 = calculate_responsiveness(toein1FPA, targetFPA)
    store_resp_RT2 = calculate_responsiveness(toein2FPA, targetFPA)
    store_resp_RT3 = calculate_responsiveness(toein3FPA, targetFPA)
    store_resp_RT4 = calculate_responsiveness(toein4FPA, targetFPA)
    store_resp_RET = calculate_responsiveness(retFPA, targetFPA)

    resp_all = [store_resp_NF, store_resp_RT1, store_resp_RT2, store_resp_RT3, store_resp_RT4, store_resp_RET]
    store_resp[subject-1] = resp_all

    # f. get proprio accuracy
    store_proprio_RMSE[subject-1] = np.sqrt(np.mean( (proprio.iloc[:,3] - proprio.iloc[:,4]) **2))
    in_inds = [1, 4, 5, 6, 8, 10, 12, 14, 16]
    out_inds = [0, 2, 3, 7, 9, 11, 13, 15, 17]
    store_proprio_MSE_out[subject-1] = np.mean( proprio.iloc[out_inds,3] - proprio.iloc[out_inds,4])
    store_proprio_MSE_in[subject-1] = np.mean( proprio.iloc[in_inds,3] - proprio.iloc[in_inds,4])

    # g. get vbtest accuracy
    store_vbtest_acc[subject-1] = np.sum(vbtest)/len(vbtest)
    if subject==4:
        store_vbtest_acc[subject-1] = 47.0/60.0 # TODO: figure out how to fix this??, the first entry is a nan instead of a 1 and nothing I do fixes it

    # h. get ROM:
    store_ROM_out[subject-1] = np.mean(ROM.iloc[0:6,2])
    store_ROM_in[subject-1] = np.mean(ROM.iloc[6:,2])

# 3. save all inputs and outputs to /features folder
# a. responsiveness
in_resp = pd.DataFrame(store_resp)
filename = os.path.normpath(os.path.join(directory, 'features\\in_resp.csv'))
in_resp.to_csv(filename, index=False)

# b. proprioception RMSE
in_proprio_RMSE = pd.DataFrame(store_proprio_RMSE)
filename = os.path.normpath(os.path.join(directory, 'features\\in_proprio_RMSE.csv'))
in_proprio_RMSE.to_csv(filename, index=False)

# c. bFPA
in_bFPA = pd.DataFrame(store_bFPA)
filename = os.path.normpath(os.path.join(directory, 'features\\in_bFPA.csv'))
in_bFPA.to_csv(filename, index=False)

# d. vb test
in_vbtest = pd.DataFrame(store_vbtest_acc)
filename = os.path.normpath(os.path.join(directory, 'features\\in_vbtest.csv'))
in_vbtest.to_csv(filename, index=False)

# e. ROM TI and TO
in_ROM_in = pd.DataFrame(store_ROM_in)
filename = os.path.normpath(os.path.join(directory, 'features\\in_ROM_in.csv'))
in_ROM_in.to_csv(filename, index=False)

in_ROM_out = pd.DataFrame(store_ROM_out)
filename = os.path.normpath(os.path.join(directory, 'features\\in_ROM_out.csv'))
in_ROM_out.to_csv(filename, index=False)

# f. proprio in/out
in_proprio_in = pd.DataFrame(store_proprio_MSE_in)
filename = os.path.normpath(os.path.join(directory, 'features\\in_proprio_in.csv'))
in_proprio_in.to_csv(filename, index=False)

in_proprio_out = pd.DataFrame(store_proprio_MSE_out)
filename = os.path.normpath(os.path.join(directory, 'features\\in_proprio_out.csv'))
in_proprio_out.to_csv(filename, index=False)


# out: rmse
out_RMSE = pd.DataFrame(store_RMSE)
filename = os.path.normpath(os.path.join(directory, 'features\\out_RMSE.csv'))
out_RMSE.to_csv(filename, index=False)

# out: error ratios
out_errRatio_in = pd.DataFrame(store_errorRatio_in)
filename = os.path.normpath(os.path.join(directory, 'features\\out_errRatio_in.csv'))
out_errRatio_in.to_csv(filename, index=False)

out_errRatio_out = pd.DataFrame(store_errorRatio_out)
filename = os.path.normpath(os.path.join(directory, 'features\\out_errRatio_out.csv'))
out_errRatio_out.to_csv(filename, index=False)

# # plot group means for cumulative results: percent steps in range
# # SF_rows = [0, 1, 6, 8, 11, 14, 18]
# SF_rows = np.where(feedbackCond_file.cond == 1)[0]
# print(SF_rows)
# print('mean SF in-range: ' + str(np.mean(store_inRangePercent[SF_rows, 5])))
# print('SD SF in-range: ' + str(np.std(store_inRangePercent[SF_rows, 5])))
# print('SF normal: stats = ' + str(stats.normaltest(store_inRangePercent[SF_rows,5])))

# # TF_rows = [2, 3, 7, 12, 15, 19, 20]
# TF_rows = np.where(feedbackCond_file.cond == 2)[0]
# print(TF_rows)
# print('mean TF in-range: ' + str(np.mean(store_inRangePercent[TF_rows, 5])))
# print('SD TF in-range: ' + str(np.std(store_inRangePercent[TF_rows, 5])))
# print('TF normal: stats = ' + str(stats.normaltest(store_inRangePercent[TF_rows,5])))

# # NF_rows = [4, 5, 9, 10, 13, 16, 17]
# NF_rows = np.where(feedbackCond_file.cond == 0)[0]
# print(NF_rows)
# print('mean NF in-range: ' + str(np.mean(store_inRangePercent[NF_rows, 5])))
# print('SD NF in-range: ' + str(np.std(store_inRangePercent[NF_rows, 5])))
# print('NF normal: stats = ' + str(stats.normaltest(store_inRangePercent[NF_rows,5])))


# # # NR 2024AUG14: output change in % acc after removing catch trials
# # print('absolute ACC: SF0-SF4: ' + str(store_inRangePercent[SF_rows,4] - store_inRangePercent[SF_rows,0])) 
# # print('TF0-TF4: ' + str(store_inRangePercent[TF_rows,4] - store_inRangePercent[TF_rows,0])) 
# # print('NF0-NF4: ' + str(store_inRangePercent[NF_rows,4] - store_inRangePercent[NF_rows,0])) 

# # print('perfect-relative ACC: SF0-SF4: ' + str((store_inRangePercent[SF_rows,4] - store_inRangePercent[SF_rows,0])/(100 - store_inRangePercent[SF_rows,0]))) 
# # print('TF0-TF4: ' + str((store_inRangePercent[TF_rows,4] - store_inRangePercent[TF_rows,0])/(100 - store_inRangePercent[TF_rows,0])))
# # print('NF0-NF4: ' + str((store_inRangePercent[NF_rows,4] - store_inRangePercent[NF_rows,0])/(100 - store_inRangePercent[NF_rows,0]))) 

# # print('absolute MAE: SF0-SF4: ' + str(store_MAE[SF_rows,4] - store_MAE[SF_rows,0])) 
# # print('TF0-TF4: ' + str(store_MAE[TF_rows,4] - store_MAE[TF_rows,0])) 
# # print('NF0-NF4: ' + str(store_MAE[NF_rows,4] - store_MAE[NF_rows,0])) 

# # print('relative MAE: SF0-SF4: ' + str((store_MAE[SF_rows,4] - store_MAE[SF_rows,0])/store_MAE[SF_rows,0])) 
# # print('TF0-TF4: ' + str((store_MAE[TF_rows,4] - store_MAE[TF_rows,0])/store_MAE[TF_rows,0])) 
# # print('NF0-NF4: ' + str((store_MAE[NF_rows,4] - store_MAE[NF_rows,0])/store_MAE[NF_rows,0])) 

# # # note: this is the same as the above rel. mae, but with signs changed
# # print('perfect-relative MAE: SF0-SF4: ' + str((store_MAE[SF_rows,4] - store_MAE[SF_rows,0])/(0 - store_MAE[SF_rows,0]))) 
# # print('TF0-TF4: ' + str((store_MAE[TF_rows,4] - store_MAE[TF_rows,0])/(0 - store_MAE[TF_rows,0])))
# # print('NF0-NF4: ' + str((store_MAE[NF_rows,4] - store_MAE[NF_rows,0])/(0 - store_MAE[NF_rows,0]))) 

# # print('######### nf vs. ret #########')
# # print('absolute MAE: SF0-SF5: ' + str(store_MAE[SF_rows,5] - store_MAE[SF_rows,0])) 
# # print('TF0-TF5: ' + str(store_MAE[TF_rows,5] - store_MAE[TF_rows,0])) 
# # print('NF0-NF5: ' + str(store_MAE[NF_rows,5] - store_MAE[NF_rows,0])) 

# # print('relative MAE: SF0-SF5: ' + str((store_MAE[SF_rows,5] - store_MAE[SF_rows,0])/store_MAE[SF_rows,0])) 
# # print('TF0-TF5: ' + str((store_MAE[TF_rows,5] - store_MAE[TF_rows,0])/store_MAE[TF_rows,0])) 
# # print('NF0-NF5: ' + str((store_MAE[NF_rows,5] - store_MAE[NF_rows,0])/store_MAE[NF_rows,0])) 

# print('##########RMSE##############')
# print('relative RMSE: SF0-SF4: ' + str((store_RMSE[SF_rows,4] - store_RMSE[SF_rows,0])/store_RMSE[SF_rows,0]))
# print('relative RMSE: TF0-TF4: ' + str((store_RMSE[TF_rows,4] - store_RMSE[TF_rows,0])/store_RMSE[TF_rows,0]))
# print('relative RMSE: NF0-NF4: ' + str((store_RMSE[NF_rows,4] - store_RMSE[NF_rows,0])/store_RMSE[NF_rows,0]))
# print('_____________________')
# print('relative RMSE: SF0-SF5: ' + str((store_RMSE[SF_rows,5] - store_RMSE[SF_rows,0])/store_RMSE[SF_rows,0]))
# print('relative RMSE: TF0-TF5: ' + str((store_RMSE[TF_rows,5] - store_RMSE[TF_rows,0])/store_RMSE[TF_rows,0]))
# print('relative RMSE: NF0-NF5: ' + str((store_RMSE[NF_rows,5] - store_RMSE[NF_rows,0])/store_RMSE[NF_rows,0]))
# print('_____________________')
# print('relative RMSE: SF4-SF5: ' + str((store_RMSE[SF_rows,5] - store_RMSE[SF_rows,4])/store_RMSE[SF_rows,4]))
# print('relative RMSE: TF4-TF5: ' + str((store_RMSE[TF_rows,5] - store_RMSE[TF_rows,4])/store_RMSE[TF_rows,4]))
# print('relative RMSE: NF4-NF5: ' + str((store_RMSE[NF_rows,5] - store_RMSE[NF_rows,4])/store_RMSE[NF_rows,4]))
# print('_____________________')
# print('NF RMSE: SF' + str(store_RMSE[SF_rows,0]))
# print('NF RMSE: TF' + str(store_RMSE[TF_rows,0]))
# print('NF RMSE: NF' + str(store_RMSE[NF_rows,0]))
# print('RT4 RMSE: SF' + str(store_RMSE[SF_rows,4]))
# print('RT4 RMSE: TF' + str(store_RMSE[TF_rows,4]))
# print('RT4 RMSE: NF' + str(store_RMSE[NF_rows,4]))
# print('RET RMSE: SF' + str(store_RMSE[SF_rows,5]))
# print('RET RMSE: TF' + str(store_RMSE[TF_rows,5]))
# print('RET RMSE: NF' + str(store_RMSE[NF_rows,5]))

# print('############# RESPONSIVENESS ###############')
# print('resp NF: SF:' + str(store_resp[SF_rows,0]))
# print('resp NF: TF:' + str(store_resp[TF_rows,0]))
# print('resp NF: NF:' + str(store_resp[NF_rows,0]))
# print('_____________________')
# print('resp RT1: SF:' + str(store_resp[SF_rows,1]))
# print('resp RT1: TF:' + str(store_resp[TF_rows,1]))
# print('resp RT1: NF:' + str(store_resp[NF_rows,1]))
# print('_____________________')
# print('resp RT4: SF:' + str(store_resp[SF_rows,4]))
# print('resp RT4: TF:' + str(store_resp[TF_rows,4]))
# print('resp RT4: NF:' + str(store_resp[NF_rows,4]))
# print('_____________________')
# print('resp RET: SF:' + str(store_resp[SF_rows,5]))
# print('resp RET: TF:' + str(store_resp[TF_rows,5]))
# print('resp RET: NF:' + str(store_resp[NF_rows,5]))
# print('_____________________')
# print('resp NF vs RT4: SF:' + str((store_resp[SF_rows,4] - store_resp[SF_rows,0])/store_resp[SF_rows,0]))
# print('resp NF vs RT4: TF:' + str((store_resp[TF_rows,4] - store_resp[TF_rows,0])/store_resp[TF_rows,0]))
# print('resp NF vs RT4: NF:' + str((store_resp[NF_rows,4] - store_resp[NF_rows,0])/store_resp[NF_rows,0]))

# # make an RMSE plot:
# fig, ax = plt.subplots(figsize = (8,6))
# sf_data = (store_RMSE[SF_rows,5] - store_RMSE[SF_rows,0])/store_RMSE[SF_rows,0]
# tf_data = (store_RMSE[TF_rows,5] - store_RMSE[TF_rows,0])/store_RMSE[TF_rows,0]
# nf_data = (store_RMSE[NF_rows,5] - store_RMSE[NF_rows,0])/store_RMSE[NF_rows,0]
# violin_parts = ax.violinplot([sf_data, tf_data, nf_data], 
#                              positions=[1, 2, 3], 
#                              showmeans=True, 
#                              showextrema=True, 
#                              showmedians=False)

# # Customize the plot
# ax.set_title('Change in RMSE between NF and Retention')
# ax.set_ylabel('Relative change in RMSE')
# ax.set_xticks([1, 2, 3])
# ax.set_xticklabels(['SF', 'TF', 'NF'])

# for i, data in enumerate([sf_data, tf_data, nf_data], start=1):
#     ax.scatter(np.random.normal(i, 0.04, len(data)), data, alpha=0.3, s=15)
# plt.show()



# x = np.arange(6)
# plt.plot(x-0.05, np.mean(store_inRangePercent[SF_rows], axis=0), '-o', color = '#05668D', label = 'SF')
# plt.errorbar(x-0.05, np.mean(store_inRangePercent[SF_rows], axis=0), yerr=np.std(store_inRangePercent[SF_rows], axis=0), fmt='none', ecolor='#05668D', capsize=5)

# plt.plot(x, np.mean(store_inRangePercent[TF_rows], axis=0), '-o', color = '#679436', label = 'TF')
# plt.errorbar(x, np.mean(store_inRangePercent[TF_rows], axis=0), yerr=np.std(store_inRangePercent[TF_rows], axis=0), fmt='none', ecolor='#679436', capsize=5)

# plt.plot(x+0.05, np.mean(store_inRangePercent[NF_rows], axis=0), '-o', color = '#805E73', label = 'NF')
# plt.errorbar(x+0.05, np.mean(store_inRangePercent[NF_rows], axis=0), yerr=np.std(store_inRangePercent[NF_rows], axis=0), fmt='none', ecolor='#805E73', capsize=5)

# plt.legend()
# plt.ylim([0,100])
# plt.ylabel('Steps within target range (%)')
# plt.show()

# # plot group means for cumulative results: percent steps in range during NF conds
# plt.plot(x, np.mean(store_inRangeNFPercent[SF_rows], axis=0), '-o', color = '#05668D', label = 'SF')
# plt.errorbar(x, np.mean(store_inRangeNFPercent[SF_rows], axis=0), yerr=np.std(store_inRangeNFPercent[SF_rows], axis=0), fmt='none', ecolor='#05668D', capsize=5)

# plt.plot(x, np.mean(store_inRangeNFPercent[TF_rows], axis=0), '-o', color = '#679436', label = 'TF')
# plt.errorbar(x, np.mean(store_inRangeNFPercent[TF_rows], axis=0), yerr=np.std(store_inRangeNFPercent[TF_rows], axis=0), fmt='none', ecolor='#679436', capsize=5)

# plt.plot(x, np.mean(store_inRangeNFPercent[NF_rows], axis=0), '-o', color = '#805E73', label = 'NF')
# plt.errorbar(x, np.mean(store_inRangeNFPercent[NF_rows], axis=0), yerr=np.std(store_inRangeNFPercent[NF_rows], axis=0), fmt='none', ecolor='#805E73', capsize=5)

# plt.legend()
# plt.ylim([0,100])
# plt.ylabel('Steps within target range during NF conds (%)')
# plt.show()

# # print mean MAEs
# print('MAE SF0: ' + str((store_MAE[SF_rows, 0])))
# print('MAE SF4: ' + str((store_MAE[SF_rows, 4])))
# print('MAE SF5: ' + str((store_MAE[SF_rows, 5])))

# print('MAE TF0: ' + str((store_MAE[TF_rows, 0])))
# print('MAE TF4: ' + str((store_MAE[TF_rows, 4])))
# print('MAE TF5: ' + str((store_MAE[TF_rows, 5])))

# print('MAE NF0: ' + str((store_MAE[NF_rows, 0])))
# print('MAE NF4: ' + str((store_MAE[NF_rows, 4])))
# print('MAE NF5: ' + str((store_MAE[NF_rows, 5])))

# # plot mean MAEs 
# plt.plot(x-0.05, np.mean(store_MAE[SF_rows], axis = 0), '-o', color = '#05668D', label = 'SF')
# plt.errorbar(x-0.05, np.mean(store_MAE[SF_rows], axis = 0), yerr=np.std(store_MAE[SF_rows], axis=0), fmt='none', ecolor='#05668D', capsize=5)

# plt.plot(x, np.mean(store_MAE[TF_rows], axis = 0), '-o', color = '#679436', label = 'TF')
# plt.errorbar(x, np.mean(store_MAE[TF_rows], axis = 0), yerr=np.std(store_MAE[TF_rows], axis=0), fmt='none', ecolor='#679436', capsize=5)

# plt.plot(x+0.05, np.mean(store_MAE[NF_rows], axis = 0), '-o', color = '#805E73', label = 'NF')
# plt.errorbar(x+0.05, np.mean(store_MAE[NF_rows], axis = 0), yerr=np.std(store_MAE[NF_rows], axis=0), fmt='none', ecolor='#805E73', capsize=5)

# plt.legend()
# plt.ylabel('MAE FPA (deg)')
# plt.show()



# # plot group means for cumulative results: mean abs error in FPA
# # plt.plot(x, np.abs(10-np.mean(store_meanFPASD[SF_rows, :, 0], axis=0)), '-o', color = '#05668D', label = 'SF')
# # plt.errorbar(x, np.abs(10-np.mean(store_meanFPASD[SF_rows, :, 0], axis=0)), yerr=np.std(store_meanFPASD[SF_rows, :, 0], axis=0), fmt='none', ecolor='#05668D', capsize=5)
# # plt.plot(x, np.abs(10-np.mean(store_meanFPASD[TF_rows, :, 0], axis=0)), '-o', color = '#679436', label = 'TF')
# # plt.errorbar(x, np.abs(10-np.mean(store_meanFPASD[TF_rows, :, 0], axis=0)), yerr=np.std(store_meanFPASD[TF_rows, :, 0], axis=0), fmt='none', ecolor='#05668D', capsize=5)
# # plt.plot(x, np.abs(10-np.mean(store_meanFPASD[NF_rows, :, 0], axis=0)), '-o', color = '#805E73', label = 'NF')
# # plt.errorbar(x, np.abs(10-np.mean(store_meanFPASD[NF_rows, :, 0], axis=0)), yerr=np.std(store_meanFPASD[NF_rows, :, 0], axis=0), fmt='none', ecolor='#05668D', capsize=5)
# # # todo: change the way i'm storing mean(SD) error 


# # plt.legend()
# # plt.ylabel('Mean FPA error (deg)')
# # plt.show()

# print('Mean (SD) percent change between first and last toe-in accuracy:')

# print('Mean SF delta: ' + str(np.mean(store_inRangePercent[SF_rows, 4] - store_inRangePercent[SF_rows,0])))
# print('SD SF delta: ' + str(np.std(store_inRangePercent[SF_rows, 4] - store_inRangePercent[SF_rows,0])))

# print('Mean TF delta: ' + str(np.mean(store_inRangePercent[TF_rows, 4] - store_inRangePercent[TF_rows,0])))
# print('SD TF delta: ' + str(np.std(store_inRangePercent[TF_rows, 4] - store_inRangePercent[TF_rows,0])))

# print('Mean NF delta: ' + str(np.mean(store_inRangePercent[NF_rows, 4] - store_inRangePercent[NF_rows,0])))
# print('SD NF delta: ' + str(np.std(store_inRangePercent[NF_rows, 4] - store_inRangePercent[NF_rows,0])))

# print('SF0: ' + str((store_inRangePercent[SF_rows, 0])))
# print('SF4: ' + str((store_inRangePercent[SF_rows, 4])))
# print('SF5: ' + str((store_inRangePercent[SF_rows, 5])))

# print('TF0: ' + str((store_inRangePercent[TF_rows, 0])))
# print('TF4: ' + str((store_inRangePercent[TF_rows, 4])))
# print('TF5: ' + str((store_inRangePercent[TF_rows, 5])))

# print('NF0: ' + str((store_inRangePercent[NF_rows, 0])))
# print('NF4: ' + str((store_inRangePercent[NF_rows, 4])))
# print('NF5: ' + str((store_inRangePercent[NF_rows, 5])))

# print('Mean (SD) percent change between last toe-in accuracy and retention:')

# print('Mean SF delta: ' + str(np.mean(store_inRangePercent[SF_rows, 5] - store_inRangePercent[SF_rows,4])))
# print('SD SF delta: ' + str(np.std(store_inRangePercent[SF_rows, 5] - store_inRangePercent[SF_rows,4])))

# print('Mean TF delta: ' + str(np.mean(store_inRangePercent[TF_rows, 5] - store_inRangePercent[TF_rows,4])))
# print('SD TF delta: ' + str(np.std(store_inRangePercent[TF_rows, 5] - store_inRangePercent[TF_rows,4])))

# print('Mean NF delta: ' + str(np.mean(store_inRangePercent[NF_rows, 5] - store_inRangePercent[NF_rows,4])))
# print('SD NF delta: ' + str(np.std(store_inRangePercent[NF_rows, 5] - store_inRangePercent[NF_rows,4])))

# # making nice figures, 2024JUL23
# # fig 1: paired scatter plots for NF, RT4, RE; 3 groups
# fig1_SF = store_MAE[SF_rows][:, [0,5]]

# x = ['NF','RE']
# base_color = '#05668D'
# colors = [to_rgba(base_color, alpha) for alpha in np.linspace(0.3, 1, 12)]

# # Transpose the data so each row becomes a line
# for i, row in enumerate(fig1_SF):
#     plt.plot(x, row, 'o-', color=colors[i])

# plt.ylim([0, 16])
# plt.xlabel('Sample')
# plt.ylabel('MAE')
# plt.title('SF')
# plt.show()

# fig1_TF = store_MAE[TF_rows][:, [0,5]]

# x = ['NF','RE']
# base_color = '#679436'
# colors = [to_rgba(base_color, alpha) for alpha in np.linspace(0.3, 1, 12)]

# # Transpose the data so each row becomes a line
# for i, row in enumerate(fig1_TF):
#     plt.plot(x, row, 'o-', color=colors[i])

# plt.ylim([0, 16])
# plt.xlabel('Sample')
# plt.ylabel('MAE')
# plt.title('TF')
# plt.show()

# fig1_NF = store_MAE[NF_rows][:, [0,5]]

# x = ['NF','RE']
# base_color = '#805E73'
# colors = [to_rgba(base_color, alpha) for alpha in np.linspace(0.3, 1, 12)]

# # Transpose the data so each row becomes a line
# for i, row in enumerate(fig1_NF):
#     plt.plot(x, row, 'o-', color=colors[i])

# plt.ylim([0, 16])
# plt.xlabel('Sample')
# plt.ylabel('MAE')
# plt.title('NF')
# plt.show()

# # Fig 2: raincloud plots

# NF_flat = store_allFPA_NF[SF_rows].reshape(1, -1).flatten()
# RT4_flat = store_allFPA_RT4[SF_rows].reshape(1, -1).flatten()
# RE_flat = store_allFPA_RET[SF_rows].reshape(1, -1).flatten()

# # Create separate DataFrames
# df_NF = pd.DataFrame({'group': 'NF', 'value': NF_flat})
# df_RT4 = pd.DataFrame({'group': 'RT4', 'value': RT4_flat})
# df_RE = pd.DataFrame({'group': 'RE', 'value': RE_flat})

# # Concatenate the DataFrames
# df_long = pd.concat([df_NF, df_RT4, df_RE], ignore_index=True)

# # Set up the figure
# f, ax = plt.subplots(figsize=(15, 8))

# custom_palette = ['#05668D', '#05668DAA', '#05668D55'] 

# # Create the raincloud plot
# pt.RainCloud(x='group', y='value', data=df_long, palette=custom_palette,
#              bw=.2, width_viol=.6, ax=ax, orient="v",
#              alpha=0.65, dodge=True, move=0.2)

# plt.title('SF: distribution of FPAs')
# plt.ylim([-25, 25])
# plt.xlabel('Columns')
# plt.ylabel('Values')
# plt.show()

# ####
# NF_flat = store_allFPA_NF[TF_rows].reshape(1, -1).flatten()
# RT4_flat = store_allFPA_RT4[TF_rows].reshape(1, -1).flatten()
# RE_flat = store_allFPA_RET[TF_rows].reshape(1, -1).flatten()

# # Create separate DataFrames
# df_NF = pd.DataFrame({'group': 'NF', 'value': NF_flat})
# df_RT4 = pd.DataFrame({'group': 'RT4', 'value': RT4_flat})
# df_RE = pd.DataFrame({'group': 'RE', 'value': RE_flat})

# # Concatenate the DataFrames
# df_long = pd.concat([df_NF, df_RT4, df_RE], ignore_index=True)

# # Set up the figure
# f, ax = plt.subplots(figsize=(15, 8))

# custom_palette = ['#679436', '#679436AA', '#67943655'] # Use the same color for all three groups

# # Create the raincloud plot
# pt.RainCloud(x='group', y='value', data=df_long, palette=custom_palette,
#              bw=.2, width_viol=.6, ax=ax, orient="v",
#              alpha=0.65, dodge=True, move=0.2)

# plt.title('TF: distribution of FPAs')
# plt.ylim([-25, 25])
# plt.xlabel('Columns')
# plt.ylabel('Values')
# plt.show()

# #############


# ####
# NF_flat = store_allFPA_NF[NF_rows].reshape(1, -1).flatten()
# RT4_flat = store_allFPA_RT4[NF_rows].reshape(1, -1).flatten()
# RE_flat = store_allFPA_RET[NF_rows].reshape(1, -1).flatten()

# # Create separate DataFrames
# df_NF = pd.DataFrame({'group': 'NF', 'value': NF_flat})
# df_RT4 = pd.DataFrame({'group': 'RT4', 'value': RT4_flat})
# df_RE = pd.DataFrame({'group': 'RE', 'value': RE_flat})

# # Concatenate the DataFrames
# df_long = pd.concat([df_NF, df_RT4, df_RE], ignore_index=True)

# # Set up the figure
# f, ax = plt.subplots(figsize=(15, 8))

# custom_palette = ['#805E73', '#805E73AA', '#805E7355'] # Use the same color for all three groups

# # Create the raincloud plot
# pt.RainCloud(x='group', y='value', data=df_long, palette=custom_palette,
#              bw=.2, width_viol=.6, ax=ax, orient="v",
#              alpha=0.65, dodge=True, move=0.2)

# plt.title('NF: distribution of FPAs')
# plt.ylim([-25, 25])
# plt.xlabel('Columns')
# plt.ylabel('Values')
# plt.show()

# # fig 3: correlation plots for TF/SF MAE, between NF and RE
# plt.scatter(store_MAE[SF_rows, 0], store_MAE[SF_rows, 5], color='#05668D')
# plt.xlabel('No-feedback toe-in')
# plt.ylabel('Retention')
# plt.xlim([1,12])
# plt.ylim([1,5])
# plt.title('SF: MAE Correlation')
# plt.show()

# plt.scatter(store_MAE[TF_rows, 0], store_MAE[TF_rows, 5], color='#679436')
# plt.xlabel('No-feedback toe-in')
# plt.xlim([1,12])
# plt.ylim([1,5])
# plt.ylabel('Retention')
# plt.title('TF: MAE Correlation')
# plt.show()
