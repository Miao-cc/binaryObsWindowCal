import sys
import numpy as np
#import matplotlib.pyplot as plt

# MJD start is 20201028
#mjdStart = 59150
#dayOffSet = [4,5,6,7]

#mjdStart = 59166
#dayOffSet = [0, 1, 2, 3]


def main():
    '''
    code for create sample MJDs for tempo2 simulate
    python getTimeSeri.py mjdStart simulateWindow sampTime
    simulateWindow: day
    sampTime: minutes
    '''
    mjdStart =  float(sys.argv[1])
    simWindow = int(sys.argv[2])
    sampTime = float(sys.argv[3])
    
    simWindow = np.arange(simWindow)
    
    
    # sample every minutes
    Nsamp = int(24*60/sampTime)
    
    sampleSeri = []
    
    for offset in simWindow:
        for i in range(Nsamp):
            timeNow = mjdStart + i*1./float(Nsamp) + offset
            sampleSeri.append(timeNow)
            print(timeNow)
    
    #for offset in simWindow:
        #for i in range(Nsamp):
           #plt.plot(sampleSeri)
    #plt.show()

if __name__ == "__main__":
    main()
