"""
This test file is meant for developing purposes. Providing an easy method to
test the functioning of PASTA during development.

"""
import pastas as ps

# read observations
fname = 'data/B32D0136001_1.csv'
obs = ps.read.dinodata(fname)

# Create the time series model
ml = ps.Model(obs.series)

# read climate data
fname = 'data/KNMI_Bilt.txt'
RH = ps.read.knmidata(fname, variable='RH')
EV24 = ps.read.knmidata(fname, variable='EV24')
#rech = RH.series - EV24.series

# Create stress
#ts = Recharge(RH.series, EV24.series, Gamma, Preferential, name='recharge')
# ts = Recharge(RH.series, EV24.series, Gamma, Combination, name='recharge')
# ts = Tseries2(RH.series, EV24.series, Gamma, name='recharge')
ts = ps.Tseries(RH.series, ps.Gamma, name='precip', freq='D')
ts1 = ps.Tseries(EV24.series, ps.Gamma, name='evap', freq='D')
ml.add_tseries(ts)
ml.add_tseries(ts1)

# Add noise model
n = ps.NoiseModel()
ml.add_noisemodel(n)

# Solve
ml.solve(weights="swsi")
ml.plot()

