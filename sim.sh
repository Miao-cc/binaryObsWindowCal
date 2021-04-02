# create the time serise
# usage: python getTimeSeri.py MJD range(day) toaIntegration(min) > C69Times.dat
python getTimeSeri.py 59305.00000000000 30 1 > J2339-0533Times.dat
ntoa=`cat J2339-0533Times.dat | wc -l `
echo ${ntoa}
# simulate the TOA
tempo2 -gr fake -f J2339-0533.par -randha y -ha 8 -rms 1e-3 -times J2339-0533Times.dat -nobs ${ntoa}
# plot the window
python ortbitPhasePlot.py J2339-0533.par J2339-0533.simulate
