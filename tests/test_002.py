import pandas as pd
from pastas import *


def test_model():
    # Import and check the observed groundwater time series
    gwdata = pd.read_csv('tests/data/B58C0698001_0.csv', skiprows=11,
                         parse_dates=['PEIL DATUM TIJD'],
                         index_col='PEIL DATUM TIJD',
                         skipinitialspace=True)
    gwdata.rename(columns={'STAND (MV)': 'h'}, inplace=True)
    gwdata.index.names = ['date']
    gwdata.h *= 0.01
    oseries = 30.17 - gwdata.h  # NAP

    # Import and check the observed precipitation series
    rain = pd.read_csv('tests/data/Heibloem_rain_data.dat', skiprows=4,
                       delim_whitespace=True,
                       parse_dates=['date'],
                       index_col='date')
    rain = rain.precip
    rain /= 1000.0  # Meters

    # Import and check the observed evaporation series
    evap = pd.read_csv('tests/data/Maastricht_E_June2015.csv', skiprows=4,
                       sep=';',
                       parse_dates=['DATE'],
                       index_col='DATE')
    evap.rename(columns={'VALUE (m-ref)': 'evap'}, inplace=True)
    evap = evap.evap

    # Create the time series model
    ml = Model(oseries)

    ts1 = Recharge(rain, evap, Gamma, Linear, name='recharge',
                   fillnan='interpolate')
    ml.add_tseries(ts1)
    n = NoiseModel()
    ml.add_noisemodel(n)

    # Solve the time series model
    ml.solve()

    return 'model succesfull'
