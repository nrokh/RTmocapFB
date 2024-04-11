import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# load pilot data
baselineFPA = pd.read_csv('I:/Shared Projects/Nataliya-Vani/Scaled Feedback Study/pilot data/pilot_21MAR2024/vsu_pilot_baselinemeanFPA1.csv')
toeinFPA = pd.read_csv('I:/Shared Projects/Nataliya-Vani/Scaled Feedback Study/pilot data/pilot_21MAR2024/vsu_pilot_meanFPA3.csv')

# combine baseline and toe-in conditions
fullFPA = pd.concat([baselineFPA, toeinFPA])

# generate plot of FPA over time
x = np.linspace(0, 300, len(fullFPA)-5)
plt.plot(x, fullFPA.iloc[5:,2], '--o')
plt.vlines(x = len(baselineFPA)+1, ymin = -15.0, ymax = 15.0)
plt.hlines(y = 4.87-10, xmin = len(baselineFPA)+1, xmax = 320)
plt.ylim([-15,15])
plt.xlabel('Time (s)')
plt.ylabel('FPA (deg)')

# save plot as svg
#plt.savefig('analysis/pilot_21MARCH2024_FPA.svg')

plt.show()

# compute mean (SD) after feedback started
print('FPA at toe-in: Mean: '+ str(np.mean(toeinFPA.iloc[:,2])) + ' SD: ' + str(np.std(toeinFPA.iloc[:,2])))

# find what % of steps fall outside a range of angles
outofrangeFPA = toeinFPA[(toeinFPA.iloc[:,2] < -4.95-3) | (toeinFPA.iloc[:,2] > -4.95+3)]
percentoutofrangeFPA = len(outofrangeFPA)/len(toeinFPA) * 100

print("percent of steps outside range: " + str(percentoutofrangeFPA))

# find what % of steps fall too far in:
outofrangeFPA = toeinFPA[(toeinFPA.iloc[:,2] < -4.95-3)]
percentoutofrangeFPA = len(outofrangeFPA)/len(toeinFPA) * 100

print("percent of steps too far in: " + str(percentoutofrangeFPA))

# find what % of steps fall too far out:
outofrangeFPA = toeinFPA[(toeinFPA.iloc[:,2] > -4.95+3)]
percentoutofrangeFPA = len(outofrangeFPA)/len(toeinFPA) * 100

print("percent of steps too far out: " + str(percentoutofrangeFPA))