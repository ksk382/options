import numpy as np
from math import sqrt, pi,log, e
from enum import Enum
import scipy.stats as stat
from scipy.stats import norm
import time
import pandas as pd

pd.set_option('display.max_rows', 800)
pd.set_option('display.min_rows', 200)


class BSMerton:
    def __init__(self, args):
        self.Type = int(args[0])  # 1 for a Call, - 1 for a put
        self.S = float(args[1])  # Underlying asset price
        self.K = float(args[2])  # Option strike K
        self.r = float(args[3])  # Continuous risk fee rate
        self.q = float(args[4])  # Dividend continuous rate
        self.T = float(args[5]) / 365.0  # Compute time to expiry
        self.sigma = float(args[6])  # Underlying volatility
        self.sigmaT = self.sigma * self.T ** 0.5  # sigma*T for reusability
        self.d1 = (log(self.S / self.K) + \
                   (self.r - self.q + 0.5 * (self.sigma ** 2)) \
                   * self.T) / self.sigmaT
        self.d2 = self.d1 - self.sigmaT
        [self.Premium] = self.premium()
        [self.Delta] = self.delta()
        [self.Theta] = self.theta()
        [self.Rho] = self.rho()
        [self.Vega] = self.vega()
        [self.Gamma] = self.gamma()
        [self.Phi] = self.phi()
        [self.Charm] = self.dDeltadTime()
        [self.Vanna] = self.dDeltadVol()

    def premium(self):
        tmpprem = self.Type * (self.S * e ** (-self.q * self.T) * norm.cdf(self.Type * self.d1) - \
                               self.K * e ** (-self.r * self.T) * norm.cdf(self.Type * self.d2))
        return [tmpprem]

    ############################################
    ############ 1st order greeks ##############
    ############################################

    def delta(self):
        dfq = e ** (-self.q * self.T)
        if self.Type == 1:
            return [dfq * norm.cdf(self.d1)]
        else:
            return [dfq * (norm.cdf(self.d1) - 1)]

    # Vega for 1% change in vol
    def vega(self):
        return [0.01 * self.S * e ** (-self.q * self.T) * \
                norm.pdf(self.d1) * self.T ** 0.5]

    # Theta for 1 day change
    def theta(self):
        df = e ** -(self.r * self.T)
        dfq = e ** (-self.q * self.T)
        tmptheta = (1.0 / 365.0) \
                   * (-0.5 * self.S * dfq * norm.pdf(self.d1) * \
                      self.sigma / (self.T ** 0.5) + \
                      self.Type * (self.q * self.S * dfq * norm.cdf(self.Type * self.d1) \
                                   - self.r * self.K * df * norm.cdf(self.Type * self.d2)))
        return [tmptheta]

    def rho(self):
        df = e ** -(self.r * self.T)
        return [self.Type * self.K * self.T * df * 0.01 * norm.cdf(self.Type * self.d2)]

    def phi(self):
        return [0.01 * -self.Type * self.T * self.S * \
                e ** (-self.q * self.T) * norm.cdf(self.Type * self.d1)]

    ############################################
    ############ 2nd order greeks ##############
    ############################################

    def gamma(self):
        return [e ** (-self.q * self.T) * norm.pdf(self.d1) / (self.S * self.sigmaT)]

    # Charm for 1 day change
    def dDeltadTime(self):
        dfq = e ** (-self.q * self.T)
        if self.Type == 1:
            return [
                (1.0 / 365.0) * -dfq * (norm.pdf(self.d1) * ((self.r - self.q) / (self.sigmaT) - self.d2 / (2 * self.T)) \
                                        + (-self.q) * norm.cdf(self.d1))]
        else:
            return [
                (1.0 / 365.0) * -dfq * (norm.pdf(self.d1) * ((self.r - self.q) / (self.sigmaT) - self.d2 / (2 * self.T)) \
                                        + self.q * norm.cdf(-self.d1))]

    # Vanna for 1% change in vol
    def dDeltadVol(self):
        return [0.01 * -e ** (-self.q * self.T) * self.d2 / self.sigma * norm.pdf(self.d1)]

    # Vomma
    def dVegadVol(self):
        return [0.01 * -e ** (-self.q * self.T) * self.d2 / self.sigma * norm.pdf(self.d1)]


if __name__ == '__main__':
    df = pd.read_csv('../option_dataframes/2021-02-07_19.04/AAPL_.csv', compression='gzip')
    print (df.head())
    x = df.loc[0]
    print (x)
    Type = 1
    S = 136.76
    K = x['strikeprice']
    r = 0
    q = 0
    T = x['days_to_expiration']
    sigma = x['imp_Volatility']
    args = [Type, S, K, r, q, T, sigma]
    a = BSMerton(args)
    print (a.delta())
    print (a.gamma())
    print (a.Charm)
    print (a.dDeltadVol())