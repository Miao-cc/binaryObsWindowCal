from __future__ import print_function, division
import sys
sys.path.append("..")

import numpy as np
import astropy.units as u
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pint.fitter
import pint.residuals
import pint.toa as toa
import pint.models as models
from pprint import pprint
from astropy.time import Time
from astropy.visualization import quantity_support

from calcwindow import *

# Turn on quantity support for plotting. This is very helpful!
quantity_support()

# load the epherm and TOA
parFileName = sys.argv[1]
timFileName = sys.argv[2]

# reading tim file and par file 
par_psr = models.get_model(parFileName)
toa_psr = toa.get_TOAs(timFileName, usepickle=False)

# get the PB
PB = par_psr.PB
firstMJD = toa_psr.first_MJD
lastMJD = toa_psr.last_MJD
RA = str(par_psr.RAJ.quantity)
DEC = str(par_psr.DECJ.quantity)
RA = RA.replace('h', ':').replace('m',':').replace('s','')
DEC = DEC.replace('d', ':').replace('m',':').replace('s','')

print("Orbit period: %s +- %s\nStart MJD: %s \nEnd MJD: %s\nRA (J2000): %s\nDEC(J2000): %s" %(PB.value, PB.uncertainty_value, firstMJD, lastMJD, RA, DEC))

FAST_trackTime = 0.21 # day

rs = pint.residuals.Residuals(toa_psr, par_psr)
toa_Bary = par_psr.get_barycentric_toas(toa_psr)
orbitPhase_Rad = par_psr.orbital_phase(toa_Bary).value

orbitPhase = orbitPhase_Rad/np.pi/2.
#index = np.logical_and(orbitPhase>(0.25-FAST_trackTime/2.), orbitPhase<(0.25+FAST_trackTime/2.))
index = np.logical_and(orbitPhase>0.225, orbitPhase<0.275)
#index = np.logical_and(orbitPhase>0.24, orbitPhase<0.26)

shapiroMJD = rs.toas.get_mjds()[index] 

#plt.errorbar(orbitPhase[index], rs.time_resids.to(u.us)[index], rs.toas.get_errors().to(u.us)[index], fmt="." )
#plt.xlim(0,0.5)
#plt.show()
#plt.errorbar(orbitPhase[index], rs.time_resids.to(u.us)[index], rs.toas.get_errors().to(u.us)[index], fmt="." )

obsTimeList = []
onWindowList = []

for mjd in range(int(firstMJD.value), int(lastMJD.value)):
    Data = Time(mjd, format='mjd').iso
    riseTime, transitTime, setTime = calcwindow(Data, RA, DEC, 36)
    riseTimeMJD = Time(str(riseTime), format='isot', scale='utc').mjd
    transitTimeMJD = Time(str(transitTime), format='isot', scale='utc').mjd
    setTimeMJD = Time(str(setTime), format='isot', scale='utc').mjd 
    obsTimeList.append([riseTimeMJD, transitTimeMJD, setTimeMJD])


#print(shapiroMJD.shape)
for mjds in obsTimeList:
    obsWindow = np.logical_and(shapiroMJD > mjds[0]*u.d, shapiroMJD < mjds[2]*u.d)
    if True in obsWindow:
        onWindowList.append(mjds)

ncols = 4
nrows = 1 + len(onWindowList)//ncols
print('ncols: %s, nrows: %s' %(ncols, nrows))

#fig = plt.figure(figsize=(25, 16))
fig = plt.figure()
gs = gridspec.GridSpec(nrows=nrows, ncols=ncols, bottom=0.05, top=0.95, left=0.05, right=0.95)
print(len(onWindowList))
for col in range(ncols):
    for row in range(nrows):
        print('cols: %s, rows: %s, num: %s' %(col, row, col*nrows+row))
        if (col*nrows+row)>=len(onWindowList):
            pass
        else:
            ax = fig.add_subplot(gs[row, col])
            ax.errorbar(rs.toas.get_mjds()[index], rs.time_resids.to(u.us)[index], yerr=rs.toas.get_errors().to(u.us)[index], fmt=".", )
            
            mjds = onWindowList[col*nrows+row]
            print(mjds)
            ax.set_xlim(mjds[0]-0.05, mjds[2]+0.05)
            ax.axvline(x=mjds[0], c="r", ls="-", lw=2)
            ax.axvline(x=mjds[1], c="r", ls="--", lw=2)
            ax.axvline(x=mjds[2], c="r", ls="-", lw=2)
            ax.text(mjds[1], 4, str(mjds[1]))
            ax.set_xlabel('')
            ax.set_ylabel('')

plt.show()
