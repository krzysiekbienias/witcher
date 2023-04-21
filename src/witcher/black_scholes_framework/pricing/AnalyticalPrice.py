from witcher.black_scholes_framework.pricing_environment.PricingEnvironment import PricingEnvironment

import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import os
import pandas as pd
from datetime import datetime
from typing import TypeVar, Iterable, Tuple, Dict, List
from enum import Enum

HM = TypeVar("HM", bound=Dict)
DT = TypeVar('DT')  # declaration HM type


class EuropeanOptionHandler():
    def __init__(self,
                 option_type: str,
                 option_strike: float,
                 option_dividend: float = 0):
        """__init__
        Description
        -----------
        This class defines and store European option parameters.

        Parameters
        ----------
        option_type : str
            style of payoff. It might be CALL or PUT.
        underlier_price : float
            Current price of underlying Asset.
        option_strike : float
            Exercise price of the option
        option_dividend : float, optional
            dividend that is paid for owner of underling, by default 0
        """
        self._option_type = option_type
        self._option_strike = option_strike
        self._option_dividend = option_dividend

        

    def __str__(self) -> str:
        return f'We created option with following attributes:'\
                f'Option Strike: {self._option_strike} \n Option Dividend {self._option_dividend}'
    
    @property
    def data(self)->HM:
        """data
        Description
        -----------
        Data method for returning the data as a dictionary object

        Returns
        -------
        _type_
            _description_
        """
        return {
            'option_type': self._option_type,
            'underlier_price': self._underlier_price,
            'option_strike': self._option_strike,
            'option_dividend': self._option_dividend
            
        }

    def get_instrinctive_value(self):
        if self._option_type == "CALL":
            return max(self._underlier_price-self._option_strike, 0)
        elif self._option_type == "PUT":
            return max(self._option_strike-self._underlier_price, 0)

        # ------------------
        # Region: Input check
        # ------------------
        if self._option_type != 'CALL' and self._option_type != 'PUT':
            raise ValueError(
                "'type_option' must be one of two values CALL or PUT")
        # ----------------------
        # End Region: Input check
        # ----------------------

class MarketEnvironment():
    def __init__(self,
                 underlier_price:float,
                 risk_free_rate:float,
                 implied_volatility:float):
        """
        Description
        -----------
        Market data object for pricing derivative instruments. It is not defined in trade attributes but comes directly from market. 

        Parameters
        ----------
        underlier_price : float

        risk_free_rate : float
            Risk fre rate for discounting
        implied_volatility : float
            Implied volatility for pricing.
        """
        self._underlier_price=underlier_price
        self._r=risk_free_rate
        self._sigma=implied_volatility

    def __str__(self) -> str:

        return f'Market data:\n Underlier Price :{self._underlier_price} \n Risk free rate for pricing :{self._r}\n Implied volatility: {self._sigma}\n '




class BlackScholesAnalyticalPrice(PricingEnvironment):

    def __init__(self,
                 option: EuropeanOptionHandler,
                 market_env:MarketEnvironment,

                 #######################
                 valuation_date: DT,
                 termination_date: DT,
                 calendar: str = 'USA',
                 year_fraction_convention: str = 'Actual365',
                 frequency: str = "Monthly",
                 **kwargs):
        self._option = option
        self._market_env=market_env
        super().__init__(valuation_date, termination_date, calendar,
                         year_fraction_convention, frequency, **kwargs)




        # --------------
        # Region: Input check
        # ---------------
        if option._option_type != 'CALL' and option._option_type != 'PUT':
            raise ValueError(
                "'type_option' must be one of two values CALL or PUT")
        if market_env._sigma <= 0:
            raise ValueError("'ann_volatility' must be positive float number.")
        # --------------
        # End Region: Input check
        # ---------------

        # --------------
        # Region: Atributes
        # ---------------
        self.black_scholes_price=self.black_scholes_price(S0=self._market_env._underlier_price,
                                                        K=self._option._option_strike,
                                                        sigma=self._market_env._sigma,
                                                        r=self._market_env._r)
        # --------------
        # Region: Atributes
        # ---------------



    def d1_helper(self,
                 option:EuropeanOptionHandler,
                 market_env:MarketEnvironment) -> float:
        """d1_helper
        Description
        -----------
        #TODO find the definition of d1.

        Parameters
        ----------
        option : EuropeanOptionHandler
            Object to store parameters that comes from contract definition.
        market_env : MarketEnvironment
            Object where we store parameters that comes from market.

        Returns
        -------
        float
            
        """

        d1 = (np.log(market_env._underlier_price / option._option_strike) + (market_env._r
            - option._option_dividend+ 0.5 * market_env._sigma ** 2) * self.year_fractions) / (
        np.sqrt(self.year_fractions) * market_env._sigma)
        return d1

    def d2_helper(self,
                 option:EuropeanOptionHandler,
                 market_env:MarketEnvironment) -> float:

        d2 = (np.log(market_env._underlier_price / option._option_strike) + (market_env._r
             - option._option_dividend -0.5 * market_env._sigma ** 2) * self.year_fractions) / (
            np.sqrt(self.year_fractions) * market_env._sigma)
        return d2

    # -----------------------
     # Region Plain Vanilla Price
     # -----------------------
    def black_scholes_price(self,
                          S0: float,
                          K: float,
                          r: float,
                          sigma: float,
                          dividend: float=0) -> float:
        """black_scholes_price
        Description
        -----------
        Theoretical price of European option within Black-Scholes framework.

        Parameters
        ----------
        S0 : float
            _description_
        K : float
            _description_
        r : float
            _description_
        sigma : float
            _description_
        dividend : float, optional
            _description_, by default 0

        Returns
        -------
        float
            European option price.
        """
        d1 = self.d1_helper(self._option,
                           self._market_env)
        d2 = self.d2_helper(self._option,
                           self._market_env)
        if (self._option._option_type == 'CALL'):
            price = S0 * np.exp(-self.year_fractions * dividend) * sc.stats.norm.cdf(d1, 0,
                                                                                 1) - K * np.exp(
                -self.year_fractions * r) * stats.norm.cdf(d2, 0, 1)
        else:
            price = K * np.exp(-self.year_fractions * r) * stats.norm.cdf(-d2, 0, 1) - \
                S0 * np.exp(-self.year_fractions * dividend) * \
                stats.norm.cdf(-d1, 0, 1)
        return price
    # --------------------------
    # End Region Plain Vanilla Price
    # --------------------------

    # -----------------------
    # Region Digital Option
    # -----------------------

    def digital_option(self,
                      S0: float,
                      K: float,
                      r: float,
                      sigma: float,
                      dividend: float=0):
        """digitalOption
        Description
        -----------
        Price of Digital option. 

        Parameters
        ----------
        S0 : float
            Current price of underlier.
        K : float
            Strike price of option.
        r : float
            risk free rate, annual
        sigma : float
            volatility, annual
        dividend : float, optional
            _description_, by default 0

        Returns
        -------
        _type_
            _description_
        """

        d1 = self.d1_helper(self._option,
                           self._market_env)
        d2 = self.d2_helper(self._option,
                           self._market_env)
        if (self._option._option_type == 'CALL'):
            price = np.exp(-self.year_fractions * r) * \
                sc.stats.norm.cdf(d1, 0, 1)
        else:
            price = np.exp(-self.year_fractions * r) * \
                sc.stats.norm.cdf(-d2, 0, 1)
        return price
    # -----------------------
    # End Region Digital Option
    # -----------------------

    def asset_or_nothing(self,
                      S0: float,
                      K: float,
                      r: float,
                      sigma: float,
                      dividend: float=0):
        d1 = self.d1_helper(self._option,
                           self._market_env)
        d2 = self.d2_helper(self._option,
                           self._market_env)
        if (self._option._option_type == 'call'):
            price = S0 * np.exp(-self.year_fractions * dividend) * sc.stats.norm.cdf(d1, 0, 1)
        else:
            price = S0 * np.exp(-self.year_fractions * dividend) * sc.stats.norm.cdf(-d1, 0, 1)
        return price


class Black76AnalyticalPrice(PricingEnvironment):
    pass 
    #TODO implement 